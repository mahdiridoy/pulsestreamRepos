#!/usr/bin/env python3
"""
Update plugins.json with new hashes and sizes from patched files.
"""
import json
import hashlib
import base64
from pathlib import Path

ROOT_DIR = Path(__file__).parent.resolve()
BUILD_DIR = ROOT_DIR / "builds"
PLUGINS_JSON = BUILD_DIR / "plugins.json"

# Read current plugins.json
with open(PLUGINS_JSON, 'r') as f:
    plugins_data = json.load(f)

# Compute actual hashes from patched .cs3 files
results = {}
for cs3_file in BUILD_DIR.glob("*.cs3"):
    if cs3_file.name == "SubscriptionManager.cs3":
        continue
    with open(cs3_file, 'rb') as f:
        data = f.read()
    sha256 = hashlib.sha256(data).digest()
    sha256_b64 = "sha256-" + base64.b64encode(sha256).decode('ascii')
    size = len(data)
    internal_name = cs3_file.stem
    results[internal_name] = (sha256_b64, size)
    print(f"{internal_name}: {sha256_b64} ({size})")

print(f"\nComputed {len(results)} hashes")

# Update plugins.json
updated = 0
for plugin in plugins_data:
    internal = plugin.get("internalName")
    if internal in results:
        sha256_b64, size = results[internal]
        plugin["fileHash"] = sha256_b64
        plugin["fileSize"] = size
        updated += 1
        print(f"  Updated {internal}: hash={sha256_b64}, size={size}")
    else:
        print(f"  No match for internalName: {internal}")

# Write back
with open(PLUGINS_JSON, 'w') as f:
    json.dump(plugins_data, f, indent=2)

print(f"\nUpdated {updated} entries in plugins.json")