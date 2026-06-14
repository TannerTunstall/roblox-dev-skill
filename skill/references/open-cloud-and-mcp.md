# Open Cloud REST APIs & Studio MCP

Two distinct integration surfaces. Don't confuse them:

| Surface | Runs | Auth | Use for |
|---|---|---|---|
| **Engine API** (Luau) | *inside* a running experience (Studio/server/client) | none (in-VM) | gameplay, DataStore, HttpService |
| **Open Cloud** (REST) | *outside* Roblox — your server, CI, tooling | API key / OAuth2 / cookie | publishing, external data access, automation |
| **Studio MCP** | bridge: your AI client ⇄ open Studio instance | localhost socket | let Claude read/edit/run the live place |

---

## Part 1 — Studio MCP (drive Studio from Claude Code)

MCP lets an AI client talk to a **live, open Roblox Studio** — read the scene, write/insert scripts, run Luau, screenshot the viewport, read the console. Studio must stay open; that's where the work happens.

### Option A — Built-in Studio MCP (recommended, since Feb 2026)
No Rust toolchain. Ships inside Studio.

1. Studio → **File → Studio Settings → Beta Features → enable "MCP Server"** (or **Assistant → Settings → MCP Servers → "Enable Studio as MCP server"**).
2. Studio listens on **`localhost:3004`** by default.
3. Use **Quick Connect** to pick your installed client (Claude Code / Claude Desktop / Cursor), or copy the JSON/CLI config it shows.
4. Keep Studio open with the target place loaded.

### Option B — Legacy standalone Rust server
`github.com/Roblox/studio-rust-mcp-server` — no longer actively developed; prefer Option A. Download a release installer, or build with `cargo run` (installs server + Studio plugin + wires Claude). Toggle it from the **Plugins** tab icon. Manual Claude Code wiring:
```sh
claude mcp add --transport stdio Roblox_Studio -- \
  '/Applications/RobloxStudioMCP.app/Contents/MacOS/rbx-studio-mcp' --stdio
```

### MCP tool surface
The exact set depends on which server you connect. Detect what's available before relying on it.

**Standard (legacy Rust server) — 6 tools:**
| Tool | Does |
|---|---|
| `run_code` | run Luau in Studio, returns output |
| `insert_model` | insert a Creator Store model |
| `get_console_output` | read console messages |
| `start_stop_play` | toggle play/server modes |
| `run_script_in_play_mode` | run a script then auto-stop |
| `get_studio_mode` | report current mode |

**Built-in / full server adds (names seen in Roblox's own Assistant skills):** `execute_luau`, `screen_capture`, `list_roblox_studios`, `set_active_studio`, `http_get` (fetch API docs as markdown), `subagent`. Community servers may add `get_file_tree`, `grep_scripts`, `create_build`.

### Canonical capability → tool map (with fallbacks)
**Never call a tool that isn't in the connected server.** Probe the available tool list first, then pick the row's available option. Community-only tools (★) often don't exist — fall back to plain Luau via `execute_luau`/`run_code`.

| Capability | Built-in / Standard (always prefer) | Community alias ★ | Offline fallback |
|---|---|---|---|
| Run Luau | `execute_luau` or `run_code` | — | output copy-paste script |
| Read/write a script's `.Source` | `execute_luau` reading/setting `script.Source` | `get_script_source` / `set_script_source` ★ | output full script + placement |
| Walk the instance tree | `execute_luau` recursive `:GetChildren()` print | `get_file_tree` / `search_objects` ★ | describe expected tree |
| Search script text | `execute_luau` loop over scripts + `string.find` | `grep_scripts` ★ | n/a |
| Start/stop a playtest | `start_stop_play` (+ `run_script_in_play_mode`) | `start_playtest` / `stop_playtest` ★ | manual F5 checklist |
| Read errors after a run | `get_console_output` | `get_playtest_output` ★ | ask user to paste Output |
| See the UI/viewport | `screen_capture` | — | ask user for a screenshot |
| Insert a model | `insert_model` | — | link Creator Store asset |
| Current mode | `get_studio_mode` | — | ask user |

Rule of thumb: anything a community tool does, **plain Luau through `execute_luau` can also do** — prefer that so the workflow runs on any server. The templates/workflows mention ★ names under "Full mode"; treat them as optional accelerators, not requirements.

### MCP working loop (interact → verify)
1. `execute_luau` / `run_code` to inspect or mutate the DataModel — **one call per logical step** to avoid races.
2. `screen_capture` to verify visual result (the only way to see PlayerGui during Play mode).
3. `get_console_output` to catch errors/warnings the change triggered.

✓ Start Play mode before anything needing a live `PlayerGui`, `UserInputService:CreateVirtualInput()`, or `SceneAnalysisService` (runtime-only).
✓ If multiple Studios are open, call `list_roblox_studios` + `set_active_studio` once at the start.
✗ `execute_luau` in **Edit** mode can't see `PlayerGui` or live `AbsolutePosition/Size` — use `screen_capture` for Play-mode UI checks.
✗ CoreGui (top bar, chat, escape menu) interactions throw — not scriptable via virtual input.

### Studio runtime helper services (for MCP-driven testing)
- **`SceneAnalysisService`** (Play mode only) — `GetInstanceCompositionAsync`, `GetTriangleCompositionAsync` (view-dependent), `GetScriptMemoryAsync`, `GetUnparentedInstancesAsync`, `GetAnimationMemoryAsync`, `GetAudioMemoryAsync`. See `performance-optimization.md`.
- **`UserInputService:CreateVirtualInput()`** (Play mode) — simulate mouse/keyboard/touch to test UI. Pair every button-down with up; screenshot after each interaction.
- **`StudioDeviceSimulatorService`** — test UI across device form factors/orientations. Portrait is where most bugs hide (UI is usually built landscape-first).

### Live docs lookup (cheapest API reference)
The MCP `http_get` tool (or your `WebFetch`) can pull any engine API page as clean markdown — use the **query** param to grep a page cheaply:
```
https://create.roblox.com/docs/reference/engine/classes/<ClassName>.md
https://create.roblox.com/docs/reference/engine/datatypes/<TypeName>.md
https://create.roblox.com/docs/reference/engine/enums/<EnumName>.md
https://create.roblox.com/docs/reference/engine/libraries/<LibName>.md
https://create.roblox.com/docs/reference/engine/deprecated.md   ← deprecated → modern map
https://create.roblox.com/docs/reference/engine/llms.txt        ← index of everything (one-liners)
```
URLs must end in `.md` (or be `llms.txt`). Don't guess API names — confirm against `llms.txt` / `api/engine-api-index.txt` first.

---

## Part 2 — Open Cloud REST API (external integrations)

Base URL **`https://apis.roblox.com`** for Open Cloud endpoints; `https://{domain}.roblox.com` for domain endpoints. Docs site `create.roblox.com` is **not** an API base.

### Auth
| Method | Header / Cookie | Env var | When |
|---|---|---|---|
| API Key | `x-api-key: <key>` | `ROBLOX_API_KEY` | most endpoints ("on Open Cloud") |
| OAuth 2.0 | `Authorization: Bearer <token>` | `ROBLOX_ACCESS_TOKEN` | user-delegated scopes |
| Cookie | `Cookie: .ROBLOSECURITY=<cookie>` | `ROBLOSECURITY` | endpoints *not* on Open Cloud |

Create keys at `create.roblox.com/dashboard/credentials` (scope the key to universe + permission). Check env vars before asking the user for credentials. Prefer Open-Cloud (key/OAuth) endpoints over cookie ones.

### Errors & paging
`401` bad/missing key · `403` key lacks scope · `404` wrong id · `429` rate-limited (exponential backoff from 1s) · `500` retry. List endpoints return `nextPageToken` → pass as `?pageToken=<v>`; stop when absent.

### Common workflows
**Upload asset (async op):**
```
POST https://apis.roblox.com/assets/v1/assets   (multipart: file + JSON metadata, x-api-key)
  → { operationId }
GET  https://apis.roblox.com/assets/v1/operations/{operationId}   poll until { done:true, response:{ assetId } }
```
**External DataStore (optimistic concurrency):**
```
GET   .../cloud/v2/universes/{u}/data-stores/{store}/entries/{entry}     → { value, etag }
PATCH .../entries/{entry}   If-Match:<etag>   { value:<new> }            ← avoids clobbering concurrent writes
```
**Publish a place from CI:**
```
POST https://apis.roblox.com/cloud/v2/universes/{u}/places/{p}/versions
  Content-Type: application/octet-stream   x-api-key:<key>   Body:<.rbxl bytes>   → { versionNumber }
```

### Feature catalog (search Features first, then Domains)
Assets · Avatars · Badges · Bans-and-blocks (`user-restrictions`) · Creator Store · Data & memory stores · Developer products · Game passes · Generative AI · Groups · Inventories · Localization · **Luau Execution** (run Luau in a cloud task) · Matchmaking · Notifications · Places · Private servers · Subscriptions · Thumbnails · Universes · Users. Full list + per-feature `.md` paths in `api/cloud-api-index.txt`.

### NOT available via REST (use Creator Dashboard)
DAU/MAU & engagement analytics · revenue/earnings/payouts · moderation history & appeals · experience ratings · Team Create permissions · marketplace fee/tax config.

### Open Cloud vs Engine — pick correctly
- Player data *inside* a game → `DataStoreService` (Engine). From an external tool → Cloud data-stores.
- HTTP from *inside* a game → `HttpService`. Call Roblox from *outside* → Open Cloud.
- Never embed an Open Cloud API key in client/Luau code that ships to players — keys are server/CI secrets only. In-experience, fetch secrets via `HttpService` from your own backend or use the Studio Secrets store, never hardcode.

> Indexes committed in `api/`: `engine-api-index.txt` (every class/enum/datatype, one-liners), `cloud-api-index.txt` (REST features+domains), `docs-index.txt` (all guide pages), `api-cheatsheet.md` (member signatures for high-traffic classes).
