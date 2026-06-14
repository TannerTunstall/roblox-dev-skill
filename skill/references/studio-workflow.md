# Roblox Studio Workflow Reference

Studio = the all-in-one IDE (Windows/Mac, free) for building, scripting, testing, publishing Roblox experiences. Every place is a **data model** (instance hierarchy). Settings: <kbd>Alt</kbd><kbd>S</kbd> / <kbd>⌥</kbd><kbd>S</kbd> (search by keyword e.g. `theme`). Shortcuts editor: **File ⟩ Customize Shortcuts** (rebind anything, including unbound actions).

## Project / place / experience structure

- **Experience** (= universe) is the published product. Contains one or more **places** (scenes/maps). One place is the **start place**. Link places via teleports (`TeleportService`).
- **Place** = one data model (`.rbxl` binary / `.rbxlx` XML). Serialization & upload happen per-place. **100 MB place file limit** — break large places into linked places if exceeded.
- **Assets** (images, meshes, audio) are cloud-based with unique asset IDs; not bundled in the place file. Reference via `rbxassetid://`.
- **Packages** = reusable instance hierarchies, updatable in one place and synced everywhere.
- Settings (name, permissions, monetization, localization, avatar) live on the **Creator Dashboard** or **File ⟩ Game/Experience Settings**. New experiences start **private**.

## Windows / panels

| Panel | Open via | Purpose |
|---|---|---|
| **Explorer** | Window / Home tab | Tree of all instances & services (the data model). Reparent by drag. |
| **Properties** | Window / Home tab | Edit selected object's properties, **Tags** (`CollectionService`), **Attributes**. |
| **Output** | Window / Script tab | `print()`, `warn()`, engine + script errors. Filter by type/context/text. Clear: <kbd>Ctrl/⌘</kbd><kbd>K</kbd>. Client msgs=blue, Server=green. |
| **Command Bar** | Script tab / Window⟩Script | Run one-off Luau. Jump: <kbd>Ctrl/⌘</kbd><kbd>9</kbd>. |
| **Asset Manager** | Window / Home tab | Manage places, images, meshes, audio; bulk import. |
| **Toolbox** | Window / Home tab | Roblox/community models, plugins, audio; your own creations & group assets. |
| **Script Editor** | Double-click a script | Full code editor (see below). |
| **Terrain Editor** | Home tab / Window⟩3D | Generate & sculpt terrain. |
| **Script Analysis** | Script tab ⟩ Analysis | Static Luau linting; errors/warnings. |
| **Breakpoints / Call Stack / Watch** | Script tab / Window⟩Debug | Debugger panels. |
| **Version History** | Window⟩Version History | Saved/published versions, notes, restore. |
| **Developer Console** | `/console` or <kbd>F9</kbd> in playtest | Client/server output, memory, network. |

**Layout:** drag header bars to dock; drag to center of a region = group as tabs; "collapse" button = pin to edge; drop with no selector = float. Customizable ribbon **tabs** (Home, Model, Avatar, UI, Script, Plugins) + custom tabs (local `.json` in `CustomRibbonTabs`).

## 3D viewport & camera

Mirrors `Workspace`. Camera: <kbd>W A S D</kbd> move, <kbd>Q E</kbd> down/up, <kbd>Shift</kbd> change speed, <kbd>F</kbd> focus selected, RMB-drag look, scroll/​<kbd>Ctrl±</kbd> zoom, MMB-drag pan, <kbd>,</kbd>/<kbd>.</kbd> rotate.
Selection: hover+click; multi-select hold <kbd>Shift</kbd>/<kbd>Ctrl</kbd>/<kbd>⌘</kbd>. **Selection cycling** (pick occluded object): hold <kbd>Alt/⌥</kbd> + click.

## Editing: transform, snapping, pivot, collisions

Transform tools (Home/Model tab): **Select** <kbd>1</kbd>, **Move** <kbd>2</kbd>, **Scale** <kbd>3</kbd>, **Rotate** <kbd>4</kbd>.
- **World vs Local orientation:** toggle <kbd>Ctrl/⌘</kbd><kbd>L</kbd> (shows **L** indicator).
- **Snapping:** increments in **studs** (move/scale) or **degrees** (rotate), set in toolbar. Hold <kbd>Shift</kbd> while dragging to **temporarily toggle** snapping. Jump to move/scale increment input <kbd>Shift</kbd><kbd>2</kbd>; rotate increment <kbd>Alt/⌥</kbd><kbd>R</kbd>.
- After a drag, the **distance indicator** stays — click it and type an exact number to fine-tune.
- **Cursor-drag move:** click a part to grab; rulers show grab/align points. While dragging: <kbd>T</kbd> tilts 90° toward camera, <kbd>R</kbd> rotates 90° around hovered surface normal. Pivot point "soft-snaps" to nearby surfaces/edges.
- Quick rotate selection: <kbd>Ctrl/⌘</kbd><kbd>T</kbd> = 90° about X, <kbd>Ctrl/⌘</kbd><kbd>R</kbd> = 90° about Y.

**Pivot** (Model tab): toggle **Pivot** to move/rotate the point objects rotate/scale around. **Edit Pivot** + **Snap** checkbox snaps to hotspots (corners/edges/centers, magenta points). **Reset** = pivot to bounding-box center. Properties: Origin Position/Orientation, Pivot Offset, World Pivot. Scripting: `:GetPivot()`, `:PivotTo(cf)`, `BasePart.PivotOffset`, `Model.WorldPivot`. Assigning `Model.PrimaryPart` moves pivot to that part; clearing it resets to center; **deleting** PrimaryPart leaves pivot in place (no jump).

**Grouping:** Model <kbd>Ctrl/⌘</kbd><kbd>G</kbd>, Folder <kbd>Ctrl/⌘</kbd><kbd>Alt/⌥</kbd><kbd>G</kbd>. Anchor/Lock/CanCollide via Home tab or Properties. (Constraints & solid modeling live in the Model tab; configurable per-instance defaults via **Edit ⟩ Save as Default [Instance]**, stored locally in `DefaultInstances.rbxm`.)

## Script Editor

- **Autocomplete:** data-model-aware (`workspace.roc` → suggests RocketShip Model), variable/function autofill, API doc pop-ups, function signatures, on-hover diagnostics. <kbd>↑</kbd>/<kbd>↓</kbd> browse, <kbd>Tab</kbd>/<kbd>Enter</kbd> accept.
- **Luau-powered:** linting/static analysis (luau.org/lint), Go to Declaration (<kbd>Ctrl/⌘</kbd>+click or <kbd>Ctrl/⌘</kbd><kbd>F12</kbd>), Script Function Filter (<kbd>Alt/⌥</kbd><kbd>F</kbd>).
- **Find/Replace** <kbd>Ctrl/⌘</kbd><kbd>F</kbd> (case/whole-word/regex). **Find/Replace All scripts** <kbd>Ctrl/⌘</kbd><kbd>Shift</kbd><kbd>F</kbd>.
- **Code Assist** (AI suggestions): auto on pause, or <kbd>Alt/⌥</kbd><kbd>\\</kbd> manual; <kbd>Tab</kbd> accept. Daily cap; needs a few lines of context; may use older APIs/Lua — review it.
- **Multi-cursor:** <kbd>Alt/⌥</kbd>+click add; <kbd>Ctrl/⌘</kbd><kbd>D</kbd> next match; <kbd>Shift</kbd><kbd>Alt/⌥</kbd><kbd>L</kbd> all matches; <kbd>Ctrl/⌘</kbd><kbd>Alt/⌥</kbd><kbd>↑/↓</kbd> above/below; <kbd>Esc</kbd> exit.
- Settings: **Script Editor** tab — font, tab width, indent-with-spaces, wrapping, color preset.

### Editor shortcuts
| Action | Win | Mac |
|---|---|---|
| Close / reopen closed script | <kbd>Ctrl</kbd><kbd>W</kbd> / <kbd>Ctrl</kbd><kbd>Shift</kbd><kbd>T</kbd> | <kbd>⌘</kbd><kbd>W</kbd> / <kbd>⌘</kbd><kbd>Shift</kbd><kbd>T</kbd> |
| Quick open | <kbd>Ctrl</kbd><kbd>P</kbd> | <kbd>⌘</kbd><kbd>P</kbd> |
| Show script in Explorer | <kbd>Ctrl</kbd><kbd>Alt</kbd><kbd>K</kbd> | <kbd>⌘</kbd><kbd>⌥</kbd><kbd>K</kbd> |
| Toggle comment | <kbd>Ctrl</kbd><kbd>/</kbd> | <kbd>⌘</kbd><kbd>/</kbd> |
| Indent / unindent | <kbd>Ctrl</kbd><kbd>]</kbd>/<kbd>[</kbd> | <kbd>⌘</kbd><kbd>]</kbd>/<kbd>[</kbd> |
| Move line up/down | <kbd>Alt</kbd><kbd>↑/↓</kbd> | <kbd>⌥</kbd><kbd>↑/↓</kbd> |
| Delete line | <kbd>Ctrl</kbd><kbd>Shift</kbd><kbd>K</kbd> | <kbd>⌘</kbd><kbd>Shift</kbd><kbd>K</kbd> |
| Format selection | <kbd>Alt</kbd><kbd>Shift</kbd><kbd>F</kbd> | <kbd>⌥</kbd><kbd>Shift</kbd><kbd>F</kbd> |
| Redo | <kbd>Ctrl</kbd><kbd>Y</kbd> | <kbd>Shift</kbd><kbd>⌘</kbd><kbd>Z</kbd> |

## Debugger

**Breakpoints** — click the gutter (red circle) or right-click for variants:
- **Standard**, **Conditional** (`var == 10`), **Logpoint** (logs `"msg", var` to Output without pausing), **Temporary** (auto-removes after one session).
- Click icon to disable (hollow); middle-click / right-click⟩Delete to remove (deletes condition/log msg — disable to keep).
- **Edit Breakpoint** options: Condition, Log Message, **Continue Execution** (don't pause), Remove-on-Hit, **Trigger At** context (Client / Server / Edit). Edits during a session persist but apply next session.

**Stepping** (mezzanine, while paused): **Step Into** <kbd>F11</kbd>, **Step Over** <kbd>F10</kbd>, **Step Out** <kbd>Shift</kbd><kbd>F11</kbd>, **Resume Scripts**, **Stop**.
**Watch:** Variables tab (in-scope vars, expand instances) + My Watches (arbitrary expressions). Add via double-click ⟩ right-click ⟩ Add Watch.
**Call Stack:** shows next line + the chain of calls and where each was called from.
**Hover** a variable in the editor while paused to see its value (e.g. a table's contents).
**Log files** on disk: Win `%LOCALAPPDATA%\Roblox\logs`; Mac `~/Library/Logs/Roblox`.

## Testing & play modes

All in left side of the **mezzanine**. **Solo** modes run **two simulations** (client + server) for accuracy.

| Mode | Shortcut | Avatar? | Notes |
|---|---|---|---|
| **Test** (Play) | <kbd>F5</kbd> | Yes, at SpawnLocation or ~(0,100,0) | Solo playtest. |
| **Test Here** (Play Here) | — | Yes, in front of current camera | Solo playtest from where you're looking. |
| **Run** | <kbd>F8</kbd> | **No avatar** | Simulates from camera pos; navigate with Studio camera. Good for observing server logic. |
| **Server & Clients** | <kbd>F7</kbd> | Yes (each client) | Multi-client: 1 server window + 1–8 client windows. Compare how clients see each other. **End Session** to close all. |
| **Team Test** | — | Yes | Live test with collaborators in cloud-saved place; one session at a time; **End Session** kicks all. |

In solo modes: **Client/Server toggle** (blue border=Client controls your char; green border=Server, free camera, char present but not controlled). Explorer shows only context-appropriate objects (e.g. `Backpack`/`PlayerScripts` exist in Client; `ServerStorage`/`ServerScriptService` scripts in Server). **Pause/Resume** (per side via dropdown) pauses physics+animations (not scripts; some `RunService` callbacks keep firing). **Step Forward** = 1/60s.
**Stop** <kbd>Shift</kbd><kbd>F5</kbd> resets all objects to pre-test state.
Other emulation: **Device** (mobile/tablet/VR), **Touch**, **Controller**, **Player Emulator** (Test menu: Locale, Pseudolocalize, Elongate, Region). **Network simulation** (Settings⟩Network: delay/jitter/loss; applies to all playtest connections; updatable live). **Party Simulator** for party APIs in Server & Clients tests.

## Command Bar

Embedded mini script editor for one-off Luau (runs at plugin/edit permission level). <kbd>Ctrl/⌘</kbd><kbd>9</kbd>. Multiline (beta): <kbd>Enter</kbd> new line, **Run** = <kbd>Ctrl/⌘</kbd><kbd>Enter</kbd>. History (last 10), saved commands (<kbd>Ctrl/⌘</kbd><kbd>B</kbd>). Supports autocomplete, linting, multi-cursor.

```lua
-- Select every unanchored BasePart in Workspace
local sel = {}
for _, d in workspace:GetDescendants() do
    if d:IsA("BasePart") and not d.Anchored then table.insert(sel, d) end
end
game:GetService("Selection"):Set(sel)
```
```lua
-- Bulk-set a property on the current selection
for _, p in game:GetService("Selection"):Get() do
    if p:IsA("BasePart") then p.Anchored = true end
end
```

## Plugins

A plugin extends Studio. Install from Creator Store/Toolbox, or build your own. Plugins run with elevated edit-mode permissions and access `plugin`, `Selection`, `ChangeHistoryService`, etc.

**Build & local-install workflow:**
1. Enable **Plugin Debugging Enabled** in Settings⟩Studio (exposes `PluginDebugService`).
2. Write the `Script`, then **Plugins menu ⟩ Save as Local Plugin** → installs into the local **Plugins** folder, appears under `PluginDebugService` and starts running.
3. ✓ Work from the copy in `PluginDebugService`; ✗ don't keep editing the source script (changes go to the wrong one). Reload: right-click ⟩ **Save and Reload Plugin**; all: <kbd>Ctrl/⌘</kbd><kbd>Shift</kbd><kbd>L</kbd>.
4. **Publish as Plugin** (Plugins menu) uploads to your inventory/Toolbox; optionally sell on Creator Store (100% net proceeds).

```lua
local toolbar = plugin:CreateToolbar("Custom")
local btn = toolbar:CreateButton("Empty Script", "Create an empty script", "rbxassetid://14978048121")
btn.ClickableWhenViewportHidden = true
btn.Click:Connect(function()
    local parent = game:GetService("Selection"):Get()[1] or game:GetService("ServerScriptService")
    local s = Instance.new("Script"); s.Source = ""; s.Parent = parent
end)
```

**Undo/redo support** — wrap mutations in `ChangeHistoryService`:
```lua
local chs = game:GetService("ChangeHistoryService")
local rec = chs:TryBeginRecording("Set neon")
if not rec then return end  -- a prior recording never finished; only one per plugin
for _, i in game:GetService("Selection"):Get() do
    if i:IsA("BasePart") then i.Material = Enum.Material.Neon end
end
chs:FinishRecording(rec, Enum.FinishRecordingOperation.Commit)
```
✗ Reloading a plugin does NOT cancel an in-flight recording — store the recording id in an attribute so reload can cancel it. ✗ Don't run always-on command-bar code that holds a recording open.

**Custom widget panels** — `plugin:CreateDockWidgetPluginGui(id, DockWidgetPluginGuiInfo.new(...))`, then parent `GuiObjects` to it. Constructor arg order: `InitialDockState, InitialEnabled, OverrideRestore, FloatX, FloatY, MinWidth, MinHeight`. ✗ Only callable from command bar or a plugin script, not regular scripts. `UserInputService` doesn't work in widgets — overlay a transparent `Frame` and use its `InputBegan`. Sync to theme via `settings().Studio.Theme:GetColor()` + `ThemeChanged`. Drag-drop: `plugin:StartDrag` + `PluginGui.PluginDragDropped`.

## Saving & publishing

| File menu action | Effect |
|---|---|
| **Save to Roblox** | Saves the place version to cloud (private; not live to players). |
| **Save to Roblox with Notes** (<kbd>Ctrl</kbd><kbd>Alt</kbd><kbd>S</kbd> / <kbd>⌘</kbd><kbd>⌥</kbd><kbd>S</kbd>) | Save + version notes for checkpoints. |
| **Save to File / Download a Copy** | Local `.rbxl` (binary, compact) or `.rbxlx` (XML, large) — for version control/external tools. |
| **Save to Roblox As** | Save into a different experience/place (used for restores). |
| **Publish (to Roblox)** | Makes the version **live**; notes required. |

- **Save ≠ Publish.** Saving updates the cloud place but players keep running the old published version. Publishing makes it live, but existing servers keep running the old version until they empty or you **restart servers** (Dashboard ⟩ Configure ⟩ Server Management; prefer "restart only outdated", optional bleed-off delay).
- **Version History** (Window⟩Version History): notes, search, filter (auto/manual/published/collaborator), restore. **Restore does NOT auto-publish** — restore opens a local copy; publish to push live.
- **Auto-recovery** files written if save fails (size limit): Win `...\RobloxStudio\AutoSaves`, Mac `.../RobloxStudio/AutoSaves/`.

## Quirks & gotchas

- ✗ **Playtest changes don't persist.** Edits during Test/Run (moving parts, new instances, property changes) are **discarded on Stop** — the data model resets to pre-test. To keep changes, copy in playtest then paste back in edit mode (right-click ⟩ Paste Into At Original Location preserves CFrame), or script-edit before playing.
- **Edit vs runtime data model differ.** Client containers (`StarterGui`→`PlayerGui`, `StarterPack`→`Backpack`, `StarterPlayerScripts`→`PlayerScripts`, `StarterCharacterScripts`→`Character`) are **copied** per-player at runtime; they don't exist as such in edit mode. `Players`/`Player`/`Backpack` only exist during play. Scripts in `ServerStorage`/`ReplicatedStorage` don't run; only `Script` in `ServerScriptService`/`Workspace` and `LocalScript` in client containers run.
- **"Only works in play mode" traps:** `Players.LocalPlayer` is nil on server & in edit; `LocalScript`/`RemoteEvent` paths, character spawning, and `Backpack` tools only resolve at runtime. Test client-only behavior under the **Client** toggle, not Server.
- **Undo / ChangeHistoryService:** editor undo is <kbd>Ctrl/⌘</kbd><kbd>Z</kbd>; plugin/programmatic mutations need explicit `ChangeHistoryService` recording to be undoable.
- **Always run latest Studio** — every experience runs the latest engine; an **Update** button appears top-right when outdated (prompts save/restart). Beta features: **File ⟩ Beta Features** (Save + restart).
- **Local-install paths** vary by machine & aren't synced to your account: plugins → Studio local Plugins folder; custom tabs → `CustomRibbonTabs` (`%LOCALAPPDATA%\Roblox\<userID>\...` Win / `~/Documents/Roblox/<userID>/...` Mac); instance defaults → `DefaultInstances.rbxm`.
- **Tags & Attributes replicate** server→client and serialize with the place; good for data-driven config without code.
- **100 MB place limit** — watch redundant parts, unoptimized terrain (horizontal layers compress best), and `CollisionFidelity` (Box/Hull cheaper than default).
- **Output colors:** blue=client, green=server; for ModuleScript output, color follows the caller's side.

### CLI (RobloxStudio.exe / RobloxStudio)
`-task EditPlace -placeId <id> -universeId <id>` open latest; `EditPlaceRevision -placeVersion <n>`; `-task EditFile -localPlaceFile <path>` (or pass `.rbxl` path positionally); `-task RunScript -runScriptFile <f> [-outputFile -quitAfterExecution]` (runs at command-bar permission; default Baseplate if no place); `-task TryAsset -assetId <id>`. Args single-dash, case-insensitive; quote paths with spaces.
