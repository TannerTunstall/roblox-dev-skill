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

**Derived from Roblox creator-docs (CC BY 4.0 — attributed to Roblox Corporation):**
- The 12 core `skill/references/*.md` deep-dives (luau-language, engine-scripting-model,
  studio-workflow, ui-ux, physics-parts-world, data-and-cloud-services, networking-and-security,
  performance-optimization, avatar-animation-audio-vfx, monetization-publishing, open-cloud-and-mcp,
  sharp-edges) are **original summaries/distillations** of the CC BY 4.0 documentation.

**Redistributed from Roblox (© Roblox Corporation):**
- `skill/api/engine-api-index.txt`, `docs-index.txt`, `cloud-api-index.txt` are copies of Roblox's
  published `llms.txt` index files.

**Generated:**
- `skill/api/api-cheatsheet.md` is generated from the community Roblox-Client-Tracker API dump.

**Original authored content (MIT, © the repository author — see LICENSE):**
- `skill/SKILL.md`, the scripts under `skill/scripts/`, `skill/guides/SETUP.md`, all of
  `skill/templates/` and `skill/workflows/`, and the reference guides `architecture-patterns.md`,
  `game-design-roblox.md`, `testing-patterns.md`, `combat-systems.md`, `inventory-systems.md`.
  These are original instructional prose and example code; they describe Roblox platform behavior but
  are not copied from Roblox's documentation.

**Not redistributed:**
- Raw upstream content (under `data/raw/`, gitignored) — the full creator-docs clone and API dumps —
  is **not** included in this repo; it is reproducible via `skill/scripts/update_docs.sh`.

## CC BY 4.0

Documentation content © Roblox Corporation, licensed under the Creative Commons Attribution 4.0
International License (https://creativecommons.org/licenses/by/4.0/). Full text:
https://github.com/Roblox/creator-docs/blob/main/LICENSE
