# PulseStream CloudStream Extension — Ad-Free Build

This repository has been modified to remove all advertisement-related code from the compiled plugins and rebranded from CNC Verse:

- **Removed:** the `omg10.com` popunder ad opened in an external browser during `loadLinks`.
- **Removed:** the "Ads Mode" subscription popup nags (`showSubscriptionPopupIfNeeded`).
- **Removed:** the Telegram promo popup (`showTelegramPopup`) and `SubscriptionHelper.showPopupIfNeeded`.
- **Removed:** the `SubscriptionManager.cs3` premium ad-removal plugin and its entry from `plugins.json`.
- **Rebranded:** `CNC Verse` → `PulseStream`, `CNC Verse Mobile` → `PulseStream Mobile`, repo shortcode `cncv` → `ps005`.

The patched builds live in [`builds/`](builds/) with fresh `fileHash`/`fileSize` values in `plugins.json`.

> **Note:** the `plugins.json`/`PulseStream.json` URLs still point to the original repo. If you host this repo yourself, replace the base URL `https://raw.githubusercontent.com/NivinCNC/CNCVerse-Cloud-Stream-Extension/builds/` with your own hosting location in both files.

### To Install Repo (Ad-Free)

Add the repo URL in CloudStream:

        https://raw.githubusercontent.com/NivinCNC/CNCVerse-Cloud-Stream-Extension/refs/heads/builds/PulseStream.json

---

### 💬 Community

Join our Telegram group to discuss extensions, request features, or report issues:  

[![Join us on Telegram](https://img.shields.io/badge/Telegram-Join%20Group-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/cncverse)

### 🕹 Tools and Programming languages used :
<p align="left">
  <a href="https://skillicons.dev">
    <img src="https://skillicons.dev/icons?i=kotlin,androidstudio,gradle,github,githubactions&theme=light&perline=5" />
  </a>
</p>

### Requirements

Cloud Stream ( To install : [View Docs](https://recloudstream.github.io/csdocs/) )

### To Install Repo

1) Direct Install : [Install](https://cutt.ly/qrQa38ja)

2) Short code : ps005

3) Manual Install (Copy and Paste in add Repo of Cloud Stream) :

        https://raw.githubusercontent.com/NivinCNC/CNCVerse-Cloud-Stream-Extension/refs/heads/builds/PulseStream.json

<!-- PLUGINS_TABLE_START -->

## 🧩 Available Plugins

| Name | Author(s) | TV Types | Version | Status |
|------|-----------|----------|---------|--------|
| AniKoto | NivinCNC | Anime, AnimeMovie, OVA | 7 | ✅ Working |
| AnimeSuge | NivinCNC | Anime, AnimeMovie, OVA | 7 | ✅ Working |
| BilibiliProvider | NivinCNC | Anime, Movies, TvSeries, Documentary | 33 | ⚠️ Geo-Restricted |
| CastleTvProvider | NivinCNC | Movie, TvSeries | 38 | ✅ Working |
| CineTvProvider | NivinCNC | Movie, TvSeries | 33 | ✅ Working |
| PulseStream | NivinCNC | Movie, TvSeries | 108 | ✅ Working |
| PulseStream Mobile | NivinCNC | Movie, TvSeries | 7 | ✅ Working |
| CricifyProvider | NivinCNC | Live | 65 | ✅ Working |
| DesiSerialsProvider | NivinCNC | TvSeries | 30 | ✅ Working |
| DoFlixProvider | NivinCNC | TvSeries, Movie | 33 | ❌ Broken |
| EinthusanProvider | NivinCNC | Movie | 35 | ✅ Working |
| GoldenAudiobook | NivinCNC | Others | 31 | ✅ Working |
| HDOProvider | NivinCNC | Movies, TvSeries | 33 | ❌ Broken |
| HDrezkaProvider | Hexated, NivinCNC | AsianDrama, Anime, TvSeries, Movie | 33 | ✅ Working |
| LibriVoxAudiobook | NivinCNC | Others | 31 | ✅ Working |
| LivXowProvider | NivinCNC | Live | 14 | ✅ Working |
| M3UPlaylistPlayerProvider | NivinCNC | Live | 15 | ✅ Working |
| MLSBDProvider | NivinCNC | Movie, TvSeries, AnimeMovie, AsianDrama | 30 | ✅ Working |
| MovieBoxProvider | NivinCNC | Movie, TvSeries | 45 | ✅ Working |
| MovieBoxProviderIN | NivinCNC | Movie, TvSeries | 47 | ✅ Working |
| MovieLinkBDProvider | NivinCNC | Movie, TvSeries, AnimeMovie, AsianDrama | 16 | ✅ Working |
| MoviezwapProvider | NivinCNC | Movie | 30 | ✅ Working |
| PikashowProvider | NivinCNC | Movie, TvSeries | 30 | ✅ Working |
| PlayFyProvider | NivinCNC | Live | 8 | ✅ Working |
| PlayZTVProvider | NivinCNC | Live | 33 | ✅ Working |
| RadioIndiaProvider | NivinCNC | Live | 31 | ✅ Working |
| Rtally | Redowan, NivinCNC | Movie, TvSeries, Anime, AnimeMovie, AsianDrama | 47 | ✅ Working |
| SKTechProvider | NivinCNC | Live | 52 | ✅ Working |
| SportzxProvider | NivinCNC | Live | 18 | ✅ Working |
| StreamFlixProvider | NivinCNC | Movie, TvSeries, Anime | 32 | ✅ Working |
| TamilDhoolProvider | NivinCNC | TvSeries | 36 | ✅ Working |
| Tamilian | NivinCNC | Movies | 30 | ✅ Working |
| TamilUltraProvider | NivinCNC | Live | 38 | ✅ Working |
| Watch32 | NivinCNC | Movie, TvSeries | 32 | ✅ Working |
| XonProvider | NivinCNC | TvSeries, Movie, Anime | 33 | ✅ Working |

*Table auto-generated on every build — 35 plugins total.*

<!-- PLUGINS_TABLE_END -->

### DMCA
We hereby issue this notice to inform you that these extensions just function like an ordinary browser (like your browser) that fetch video files from internet,
and do not violate the provisions of the Digital Millennium Copyright Act (DMCA). 
The Content these extensions may access is not hosted by us or the Cloudstream 3 application but the websites they are browsing in their autonomous mode. It is sole responsibility 
of the user and his/her countries' or states' law. If you think they are violating any intellectual property then please contact the actual file hosts not the owners of this repository or the CloudStream 3 app.

Thank You.

