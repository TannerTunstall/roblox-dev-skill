# Setup Guide — roblox-dev-skill

Everything needed to go from zero to an AI-assisted Roblox dev loop. Read top to bottom the first time; skip to a section after that.

---

## 0. What you get

- A **Claude Code skill** (`skill/`) that makes the assistant a Roblox expert: Luau, Studio, engine APIs, UI/UX, networking/security, data, performance, monetization, MCP.
- Committed **API indexes** (`skill/api/`) — every class/enum/datatype + REST surface, current as of the engine version recorded in `skill/api/STUDIO_VERSION`.
- An **update script** (`skill/scripts/update_docs.sh`) to re-pull docs and regenerate the indexes when Roblox ships changes.

You need three things working: (1) the skill installed, (2) Roblox Studio + the MCP bridge, (3) optionally an external toolchain (Rojo etc.) if you want a real codebase instead of editing scripts inside Studio.

---

## 1. Install the skill

Claude Code loads skills from `~/.claude/skills/<name>/SKILL.md`.

```sh
# from the repo root
ln -s "$(pwd)/skill" ~/.claude/skills/roblox-dev
#   …or copy if you prefer:  cp -R skill ~/.claude/skills/roblox-dev
```
Restart Claude Code (or `/skills` to confirm it's listed). Invoke with `/roblox-dev` or just describe a Roblox task — the skill's description triggers it.

> Project-local alternative: put it at `<project>/.claude/skills/roblox-dev/` to scope it to one game repo.

---

## 2. Roblox Studio + MCP (the live bridge)

This is what lets the assistant read your scene, write scripts, run Luau, and screenshot the viewport in the *actual* place you have open.

### Recommended: built-in Studio MCP (no toolchain)
1. Install **Roblox Studio** and open it once.
2. **File → Studio Settings → Beta Features → enable "MCP Server"** (or **Assistant → Settings → MCP Servers → "Enable Studio as MCP server"**).
3. Studio now listens on **`localhost:3004`**.
4. Use **Quick Connect** in that settings panel to pick **Claude Code**, or copy the CLI/JSON it shows.
5. **Keep Studio open** with your place loaded whenever you want live edits.

### Legacy: standalone Rust MCP server
Only if the built-in one isn't available. `github.com/Roblox/studio-rust-mcp-server` → download the release installer (or `cargo run` to build). Then wire Claude Code:
```sh
claude mcp add --transport stdio Roblox_Studio -- \
  '/Applications/RobloxStudioMCP.app/Contents/MacOS/rbx-studio-mcp' --stdio
```
Toggle the bridge from the **Plugins** tab icon in Studio.

### Verify the connection
In Claude Code: "run `print(workspace:GetChildren())` in Studio." You should get the live child list back. If not: Studio open? Bridge toggled on? Right client selected in Quick Connect?

> See `references/open-cloud-and-mcp.md` for the full tool list and the interact→verify loop.

---

## 3. External toolchain (optional but recommended for real projects)

Editing scripts inside Studio is fine for prototypes. For a maintainable codebase with version control, AI editing, and CI, sync files from disk into Studio with **Rojo**. Manage all these tools with one version manager.

### Toolchain manager — Rokit (or Aftman)
[Rokit](https://github.com/rojo-rbx/rokit) pins tool versions per project in `rokit.toml`.
```sh
# macOS
brew install rokit    # or: curl -fsSL https://raw.githubusercontent.com/rojo-rbx/rokit/main/scripts/install.sh | sh
rokit init
rokit add rojo-rbx/rojo
rokit add rojo-rbx/tarmac        # asset sync (optional)
rokit add johnnymorganz/stylua   # formatter
rokit add kampfkarren/selene     # linter
rokit install
```

### The core tools
| Tool | Role | Why |
|---|---|---|
| **Rojo** | sync `src/` ↔ Studio | edit Luau as real files, use git + the assistant |
| **Wally** | package manager (`wally.toml`) | pull community libs (Roact/React-lua, Fusion, Promise, Signal, ProfileStore) |
| **StyLua** | formatter | consistent style; run on save / pre-commit |
| **selene** | static linter | catches bugs & bad patterns (`selene src/`) |
| **Luau LSP** | editor intellisense | autocomplete/type-check in VS Code (`JohnnyMorganz.luau-lsp`) |
| **Lune** | standalone Luau runtime | run build/test scripts outside Studio |
| **Argon** | Rojo-compatible sync + 2-way | alternative to Rojo with bidirectional sync |

### Minimal Rojo project
`default.project.json`:
```json
{
  "name": "MyGame",
  "tree": {
    "$className": "DataModel",
    "ReplicatedStorage": { "Shared": { "$path": "src/shared" } },
    "ServerScriptService": { "Server": { "$path": "src/server" } },
    "StarterPlayer": {
      "StarterPlayerScripts": { "Client": { "$path": "src/client" } }
    }
  }
}
```
File suffixes map to instance types: `.server.luau` → Script, `.client.luau` → LocalScript, `.luau` → ModuleScript, `init.luau` in a folder → that folder becomes a ModuleScript.
```sh
rojo serve            # then in Studio: Plugins → Rojo → Connect (install the Rojo plugin once)
```
Now the assistant edits files in `src/`, Rojo pushes them into Studio live, and you `git commit` real source.

> VS Code: install **Rojo** + **Luau Language Server** extensions. Recommended `.vscode/settings.json` enables `luau-lsp` with the Rojo `sourcemap` for accurate types (`rojo sourcemap default.project.json -o sourcemap.json --watch`).

---

## 4. Open Cloud (only for external automation / CI)
If you want to publish from CI, manage DataStores externally, or hit Roblox REST APIs:
1. Create an API key at `create.roblox.com/dashboard/credentials`, scoped to your universe + the permissions you need.
2. Export it: `export ROBLOX_API_KEY=...` (never commit it; never ship it in Luau).
3. See `references/open-cloud-and-mcp.md` Part 2 and `api/cloud-api-index.txt`.

---

## 5. Recommended day-to-day loop
1. Open Studio with your place; MCP bridge on; `rojo serve` running (if using files).
2. Tell the assistant what you want ("add a server-validated coin shop", "fix the leaderboard UI on mobile").
3. It writes/edits code (files via Rojo, or directly via MCP `execute_luau`), runs it in Studio, reads the console, and screenshots to verify.
4. Playtest (**F5**), iterate. Commit when happy.

---

## 6. Keeping the knowledge current
Roblox ships engine updates roughly weekly. To refresh the committed API indexes & cheat-sheet:
```sh
./skill/scripts/update_docs.sh      # re-clones docs, re-pulls API dump + llms indexes, regenerates cheat-sheet
```
The reference `.md` files are hand-distilled; re-run the distillation (or ask the assistant to) only when a major platform change lands. `skill/api/STUDIO_VERSION` records the engine version the current indexes were built from.

---

## 7. Troubleshooting
| Symptom | Fix |
|---|---|
| Skill not triggering | `~/.claude/skills/roblox-dev/SKILL.md` exists? Restart Claude Code; check `/skills`. |
| MCP calls fail | Studio open + place loaded? Bridge toggled on? Correct client in Quick Connect? Port 3004 free? |
| `execute_luau` can't see PlayerGui | You're in Edit mode — start Play mode, or use `screen_capture`. |
| Rojo won't connect | Rojo Studio plugin installed? `rojo serve` running? Versions match (`rojo --version` vs plugin)? |
| Types/autocomplete wrong | Regenerate `sourcemap.json` and reload the Luau LSP. |
| DataStores fail in Studio | Game Settings → Security → "Enable Studio Access to API Services". |
