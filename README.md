# roblox-dev-skill

A self-contained **Claude Code skill** that makes the assistant think and work like a **senior Roblox
game developer** — distilled from the *complete* official Roblox creator documentation, plus the
machine-readable Engine API dump and Open Cloud REST surface, with genre build templates and audit
workflows.

The goal: maximum Roblox knowledge at minimum token cost. The full docs are analyzed and compressed into a
lean router + focused reference files (progressive disclosure), with current API indexes committed for offline
lookup and an update script to re-pull when Roblox ships changes. When connected to Roblox Studio via MCP,
the skill doesn't just write code — it builds, runs, reads the console, and fixes until the feature works.

> **License:** MIT for original content · portions derived from Roblox creator-docs under CC BY 4.0.
> See [LICENSE](LICENSE) and [NOTICE.md](NOTICE.md).
> **Not affiliated with or endorsed by Roblox Corporation.** "Roblox", "Roblox Studio", and "Luau" are
> trademarks of Roblox Corporation.

## What's inside

```
skill/
  SKILL.md                     # senior-dev router: mindset, execution loop, routing, non-negotiables
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
    open-cloud-and-mcp.md      #   Studio MCP (built-in + legacy) + capability→tool map + Open Cloud REST
    sharp-edges.md             #   cross-cutting gotchas — scan when something's mysteriously broken
    architecture-patterns.md   #   senior structure: service/module patterns, init, anti-patterns
    game-design-roblox.md      #   core loop, progression, retention, monetization design
    combat-systems.md          #   weapons, damage, hit detection (server-authoritative)
    inventory-systems.md       #   items, equipment, stacking, persistence
    testing-patterns.md        #   verification, TestEZ-style specs, integration testing
  templates/                   # build-a-game scaffolds (loaded when building)
    game-scaffold.md           #   universal base: DataManager (pcall/UpdateAsync/session-lock/BindToClose), remotes, loading
    genre-{simulator,tycoon,obby,rpg,horror,battle-royale}.md  # genre-specific systems
  workflows/                   # opinionated multi-step procedures (loaded by task)
    new-game.md                #   genre→scope→architecture→scaffold→systems→MCP build/test/fix→summary
    debug-loop.md  code-review.md  security-audit.md  performance-audit.md
    monetization-audit.md  publish-checklist.md
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
4. Merged in genre templates, audit workflows, and senior-thinking references (architecture,
   game design, testing, combat, inventory) from the prior `roblox-game` skill — remapping all
   cross-links, reconciling MCP tool names to the verified toolset, and sanity-checking every link,
   code fence, and idiom.

## Keeping current
Roblox updates the engine ~weekly. Run `./skill/scripts/update_docs.sh` to refresh the committed
indexes and cheat-sheet. Re-distill the prose references only after a major platform change.

## Attribution & license
- **Original content** (SKILL.md, scripts, templates, workflows, the hand-authored reference guides) —
  **MIT**, see [LICENSE](LICENSE).
- **Derived/redistributed from Roblox creator-docs** (the 12 core reference distillations and the
  `api/*.txt` indexes) — documentation content © Roblox Corporation, licensed **CC BY 4.0**.
- The Engine API dump (`api-cheatsheet.md` source) comes from the community **Roblox-Client-Tracker**.
- Full breakdown of what is original vs. derived: [NOTICE.md](NOTICE.md).

Not affiliated with or endorsed by Roblox Corporation. Provided "as is" with no warranty.

## Contributing / using
Clone it, symlink `skill/` into `~/.claude/skills/`, and you're set (see
[skill/guides/SETUP.md](skill/guides/SETUP.md)). Issues and PRs welcome. Run
`./skill/scripts/update_docs.sh` to refresh against the latest engine release.
