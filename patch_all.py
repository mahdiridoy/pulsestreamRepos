#!/usr/bin/env python3
"""
Patch all .cs3 plugins to remove ads/popups/CSGuard.
Works on Linux (GitHub Actions) and Windows.
"""
import os
import sys
import re
import zipfile
import hashlib
import base64
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

# Configuration - use relative paths
ROOT_DIR = Path(__file__).parent.resolve()
BUILD_DIR = ROOT_DIR / "builds"
TOOLS_DIR = ROOT_DIR / "tools" / "smali"
BAKSMALI_JAR = TOOLS_DIR / "baksmali-2.4.0.jar"
SMALI_JAR = TOOLS_DIR / "smali-2.4.0.jar"
JAVA = "java"

# Target methods to patch
# Provider class methods (private final instance methods)
PROVIDER_METHODS = {
    'openInExternalBrowser(Ljava/lang/String;)V': ('return-void', None),
    'showSubscriptionPopupIfNeeded()V': ('return-void', None),
    'showTelegramPopup()V': ('return-void', None),
}
# Companion class methods
COMPANION_METHODS = {
    'isCsGuardBlocked()Z': ('const/4 v0, 0x0', 'return v0'),  # return false
    'showCsGuardToast(Landroid/content/Context;)V': ('return-void', None),
}
# Also patch loadLinks$lambda$0$0 (the "Opening ads" toast)
STATIC_LAMBDA_METHODS = {
    'loadLinks\\$lambda\\$0\\$0\\(Landroid/content/Context;\\)V': ('return-void', None),
}

def run_cmd(cmd, cwd=None):
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=180)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}\n{result.stderr}")
    return result.stdout

def patch_smali_file(smali_path):
    """Patch a single .smali file in place."""
    with open(smali_path, 'r') as f:
        lines = f.readlines()
    
    new_lines = []
    in_target_method = False
    method_type = None  # 'provider', 'companion', 'static_lambda'
    method_name = None
    body_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        if not in_target_method:
            # Check for method start
            m = re.match(r'^(\.method\s+(?:private|public)\s+(?:final\s+)?(?:static\s+)?(?:synthetic\s+)?)(\S+)', line)
            if m:
                method_sig = m.group(2)
                
                is_static = 'static' in m.group(1)
                is_final = 'final' in m.group(1)
                is_private = 'private' in m.group(1)
                is_public = 'public' in m.group(1)
                
                # Provider: private final (instance, not static)
                if not is_static and is_final and is_private and method_sig in PROVIDER_METHODS:
                    in_target_method = True
                    method_type = 'provider'
                    method_name = method_sig
                    new_lines.append(line)
                    i += 1
                    continue
                
                # Companion: public final isCsGuardBlocked()Z (instance) or private final showCsGuardToast
                if not is_static and is_final and (is_public or is_private) and method_sig in COMPANION_METHODS:
                    in_target_method = True
                    method_type = 'companion'
                    method_name = method_sig
                    new_lines.append(line)
                    i += 1
                    continue
                
                # Static lambda: private static final loadLinks$lambda$0$0
                if is_static and is_final and is_private:
                    for pattern, (insn1, insn2) in STATIC_LAMBDA_METHODS.items():
                        if re.match(pattern, method_sig):
                            in_target_method = True
                            method_type = 'static_lambda'
                            method_name = method_sig
                            body_lines = [insn1] if insn1 else []
                            if insn2:
                                body_lines.append(insn2)
                            new_lines.append(line)
                            i += 1
                            continue
            
            new_lines.append(line)
            i += 1
        else:
            # Inside target method - skip until .end method
            if line.strip() == '.end method':
                # Emit patched body
                if method_type == 'provider':
                    # Keep original .registers, add return-void
                    orig_regs = None
                    for bl in body_lines:
                        m = re.match(r'^\s*\.registers\s+(\d+)', bl)
                        if m:
                            orig_regs = m.group(1)
                            break
                    if orig_regs:
                        new_lines.append(f'    .registers {orig_regs}\n')
                    else:
                        new_lines.append('    .registers 10\n')
                    new_lines.append('    return-void\n')
                elif method_type == 'companion':
                    if method_name == 'isCsGuardBlocked()Z':
                        new_lines.append('    .registers 2\n')
                        new_lines.append('    const/4 v0, 0x0\n')
                        new_lines.append('    return v0\n')
                    else:  # showCsGuardToast
                        new_lines.append('    .registers 5\n')
                        new_lines.append('    return-void\n')
                elif method_type == 'static_lambda':
                    new_lines.append('    .registers 3\n')
                    for bl in body_lines:
                        new_lines.append(f'    {bl}\n')
                
                new_lines.append(line)
                in_target_method = False
                method_type = None
                method_name = None
                body_lines = []
            else:
                # Collect original body to extract .registers
                body_lines.append(line)
            i += 1
    
    with open(smali_path, 'w') as f:
        f.writelines(new_lines)
    return True

def patch_cs3(cs3_path, work_dir):
    """Patch a single .cs3 file. Returns (new_sha256_b64, new_size)."""
    cs3_name = cs3_path.name
    print(f"\n=== Patching {cs3_name} ===")
    
    # Extract zip
    extract_dir = work_dir / "extract"
    if extract_dir.exists():
        shutil.rmtree(extract_dir)
    extract_dir.mkdir(parents=True)
    
    with zipfile.ZipFile(cs3_path, 'r') as z:
        z.extractall(extract_dir)
    
    # Find classes.dex
    dex_path = extract_dir / "classes.dex"
    if not dex_path.exists():
        raise FileNotFoundError(f"classes.dex not found in {cs3_name}")
    
    # Disassemble
    smali_dir = work_dir / "smali"
    if smali_dir.exists():
        shutil.rmtree(smali_dir)
    run_cmd([JAVA, "-jar", str(BAKSMALI_JAR), "d", str(dex_path), "-o", str(smali_dir)])
    
    # Patch all smali files
    for smali_file in smali_dir.rglob("*.smali"):
        patch_smali_file(smali_file)
    
    # Reassemble
    new_dex = work_dir / "classes_patched.dex"
    run_cmd([JAVA, "-jar", str(SMALI_JAR), "a", str(smali_dir), "-o", str(new_dex)])
    
    # Replace classes.dex in extract_dir
    shutil.copy2(new_dex, dex_path)
    
    # Repack zip (preserve all original files, just replace classes.dex)
    with zipfile.ZipFile(cs3_path, 'w', zipfile.ZIP_DEFLATED) as z:
        for root, dirs, files in os.walk(extract_dir):
            for file in files:
                full = Path(root) / file
                arc = full.relative_to(extract_dir)
                z.write(full, arc)
    
    # Compute new hash and size
    with open(cs3_path, 'rb') as f:
        data = f.read()
    sha256 = hashlib.sha256(data).digest()
    sha256_b64 = "sha256-" + base64.b64encode(sha256).decode('ascii')
    size = len(data)
    
    print(f"  New hash: {sha256_b64}")
    print(f"  New size: {size}")
    return sha256_b64, size

def main():
    # Get list of .cs3 files to patch (skip SubscriptionManager)
    cs3_files = sorted([f for f in BUILD_DIR.glob("*.cs3") if f.name != "SubscriptionManager.cs3"])
    print(f"Found {len(cs3_files)} plugins to patch")
    
    plugins_json = BUILD_DIR / "plugins.json"
    with open(plugins_json, 'r') as f:
        plugins_data = json.load(f)
    
    # Create backup
    shutil.copy2(plugins_json, plugins_json.with_suffix('.json.bak'))
    
    # Patch each plugin
    results = {}
    with tempfile.TemporaryDirectory(prefix="patch_") as tmp:
        work_base = Path(tmp)
        for cs3_path in cs3_files:
            try:
                work_dir = work_base / cs3_path.stem
                work_dir.mkdir()
                sha256_b64, size = patch_cs3(cs3_path, work_dir)
                results[cs3_path.name] = (sha256_b64, size)
            except Exception as e:
                print(f"  ERROR patching {cs3_path.name}: {e}")
                raise
    
    # Update plugins.json
    print("\n=== Updating plugins.json ===")
    for plugin in plugins_data:
        internal = plugin.get("internalName")
        cs3_name = f"{internal}.cs3"
        if cs3_name in results:
            sha256_b64, size = results[cs3_name]
            plugin["fileHash"] = sha256_b64
            plugin["fileSize"] = size
            print(f"  Updated {internal}: hash={sha256_b64}, size={size}")
        else:
            print(f"  Skipped (no patch result): {internal}")
    
    with open(plugins_json, 'w') as f:
        json.dump(plugins_data, f, indent=2)
    
    print("\n=== Done ===")

if __name__ == "__main__":
    main()