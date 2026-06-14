# roblox-dev-skill

A private, self-contained **Claude Code skill** that turns the assistant into an expert Roblox
creator — distilled from the *complete* official Roblox creator documentation, plus the machine-readable
Engine API dump and Open Cloud REST surface.

The goal: maximum Roblox knowledge at minimum token cost. The full docs are analyzed and compressed into a
lean router + focused reference files (progressive disclosure), with current API indexes committed for offline
lookup and an update script to re-pull when Roblox ships changes.

## What's inside

```
skill/
  SKILL.md                     # lean router + non-negotiables + API lookup protocol (the entry point)
  references/                  # dense, token-efficient deep-dives (loaded on demand)
    luau-language.md           #   Luau: types, tables/metatables, OOP, task lib, perf idioms, quirks
    engine-scripting-model.md  #   DataModel, services, scripts/RunContext, replication, events, Actors
    studio-workflow.md         #   Studio IDE, panels, testing modes, plugins, Command Bar, quirks
    ui-ux.md                   #   GUI objects, UDim2/layout, responsive, cross-platform input, UX
    physics-parts-world.md     #   parts, CFrame math, constraints, raycasting, network ownership, terrain
    data-and-cloud-services.md #   DataStore/MemoryStore/Messaging, session-locking, teleport/matchmaking
    networking-and-security.md #   Remotes, replication, never-trust-client, validation, anti-cheat
    performance-optimization.md#   budgets, profiling, rendering, streaming, memory leaks, triage table
    avatar-animation-audio-vfx.md # Humanoid, animation, avatars, audio, particles/VFX
    monetization-publishing.md #   passes/products/receipts/subs, publishing, analytics, moderation, i18n
    open-cloud-and-mcp.md      #   Studio MCP (built-in + legacy) and Open Cloud REST
    sharp-edges.md             #   cross-cutting gotchas — scan when something's mysteriously broken
  api/                         # current, committed lookup indexes (offline)
    engine-api-index.txt       #   every class/enum/datatype/global/library, one-line summaries (llms.txt)
    api-cheatsheet.md          #   concrete member signatures for high-traffic classes (generated)
    cloud-api-index.txt        #   Open Cloud REST features + domains
    docs-index.txt             #   index of all guide pages
    STUDIO_VERSION             #   engine version the indexes were built from
  guides/
    SETUP.md                   # install the skill, Studio MCP, Rojo/Rokit/Wally/StyLua toolchain, Open Cloud
  scripts/
    update_docs.sh             # re-pull docs + API dump + indexes, regenerate cheat-sheet
    build_api_cheatsheet.py    # API-Dump.json → api/api-cheatsheet.md
data/raw/                      # full source clone + API dumps (gitignored — reproduce via update_docs.sh)
```

## Install & use
See **[skill/guides/SETUP.md](skill/guides/SETUP.md)**. Quick start:
```sh
ln -s "$(pwd)/skill" ~/.claude/skills/roblox-dev   # then restart Claude Code
```
Invoke with `/roblox-dev` or just describe a Roblox task.

## How it was built
1. Cloned `github.com/Roblox/creator-docs` (978 guide pages) + pulled the Engine API dump
   (886 classes / 588 enums) and the live `llms.txt` indexes.
2. Analyzed the corpus and fanned out per-topic distillation into the dense `references/` files.
3. Generated the offline API cheat-sheet from the dump; committed the compact indexes.

## Keeping current
Roblox updates the engine ~weekly. Run `./skill/scripts/update_docs.sh` to refresh the committed
indexes and cheat-sheet. Re-distill the prose references only after a major platform change.

## Attribution & license
Derived from Roblox **creator-docs** — documentation content licensed **CC BY 4.0**, code **MIT**
(© Roblox Corporation). See [NOTICE.md](NOTICE.md). The Engine API dump comes from the community
**Roblox-Client-Tracker**. This repository is a private derivative for personal development use.
