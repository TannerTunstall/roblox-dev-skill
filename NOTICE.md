# Attribution & Licensing

This repository contains material **derived from** the official Roblox creator documentation and
related community data sources. It is a private derivative for personal development use.

## Sources

| Source | Repository / URL | License |
|---|---|---|
| Roblox creator documentation (prose & guides) | https://github.com/Roblox/creator-docs | Content: **CC BY 4.0** |
| Roblox creator-docs code/tools | https://github.com/Roblox/creator-docs | Code: **MIT** |
| Live API/doc indexes (`llms.txt`) | https://create.roblox.com/docs | © Roblox Corporation |
| Engine API dump (`API-Dump.json`) | https://github.com/MaximumADHD/Roblox-Client-Tracker | Community-maintained mirror of Roblox API metadata |
| Bundled Studio Assistant skills (referenced) | `creator-docs/skills/` | © Roblox Corporation |

"Roblox", "Roblox Studio", and "Luau" are trademarks of Roblox Corporation. This project is not
affiliated with or endorsed by Roblox Corporation.

## What is derived vs. original

- The `skill/references/*.md` files are **original distillations/summaries** written from the CC BY 4.0
  documentation. Per CC BY 4.0, attribution is given here to Roblox Corporation as the source.
- The `skill/api/*.txt` indexes are copies of Roblox's published `llms.txt` index files.
- `skill/api/api-cheatsheet.md` is generated from the community API dump.
- Raw upstream content (under `data/raw/`, gitignored) is **not** redistributed in this repo; it is
  reproducible via `skill/scripts/update_docs.sh`.

## CC BY 4.0

Documentation content © Roblox Corporation, licensed under the Creative Commons Attribution 4.0
International License (https://creativecommons.org/licenses/by/4.0/). Full text:
https://github.com/Roblox/creator-docs/blob/main/LICENSE
