#!/usr/bin/env python3
"""Build a compact, token-efficient API cheat-sheet from the Roblox API dump.

Input : data/raw/API-Dump.json  (full machine-readable engine dump)
Output: skill/api/api-cheatsheet.md

Strategy: the live llms.txt indexes already give one-line summaries for *every*
API, and full per-API docs are a WebFetch away. So this cheat-sheet does what
those indexes do NOT: it lists the concrete member signatures (properties /
methods / events) for a curated set of the highest-traffic classes, services,
and datatypes — the ones a dev touches every day — so they are available
offline without fetching. Deprecated / non-scriptable members are dropped.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DUMP = os.path.join(ROOT, "data", "raw", "API-Dump.json")
OUT = os.path.join(ROOT, "skill", "api", "api-cheatsheet.md")

# Curated high-value classes/services. Members of these get fully listed.
CURATED = [
    # Core services
    "Workspace", "Players", "Player", "ReplicatedStorage", "ServerStorage",
    "ServerScriptService", "StarterGui", "StarterPack", "StarterPlayer",
    "Lighting", "SoundService", "RunService", "UserInputService",
    "ContextActionService", "TweenService", "Debris", "CollectionService",
    "PhysicsService", "TeleportService", "DataStoreService", "MemoryStoreService",
    "MessagingService", "HttpService", "MarketplaceService", "BadgeService",
    "GamePassService", "PathfindingService", "Teams", "Chat", "TextChatService",
    "ProximityPromptService", "ContentProvider", "ReplicatedFirst",
    "GuiService", "StarterPlayerScripts", "StarterCharacterScripts",
    "AnalyticsService", "PolicyService", "GroupService", "AssetService",
    "TextService", "LocalizationService", "HapticService", "VRService",
    # Core instances
    "Instance", "BasePart", "Part", "MeshPart", "Model", "Humanoid",
    "HumanoidDescription", "Animator", "Animation", "AnimationTrack",
    "Tool", "Accessory", "Attachment", "Sound", "ParticleEmitter",
    "Beam", "Trail", "Light", "PointLight", "SpotLight", "SurfaceLight",
    "ProximityPrompt", "ClickDetector", "Camera",
    # Scripts
    "Script", "LocalScript", "ModuleScript", "BaseScript", "LuaSourceContainer",
    # Networking
    "RemoteEvent", "RemoteFunction", "BindableEvent", "BindableFunction",
    "UnreliableRemoteEvent", "Actor",
    # Values
    "ValueBase", "IntValue", "StringValue", "BoolValue", "NumberValue",
    "ObjectValue", "CFrameValue", "Vector3Value", "Color3Value",
    # GUI
    "GuiObject", "GuiBase2d", "ScreenGui", "Frame", "TextLabel", "TextButton",
    "TextBox", "ImageLabel", "ImageButton", "ScrollingFrame", "CanvasGroup",
    "UICorner", "UIPadding", "UIListLayout", "UIGridLayout", "UITableLayout",
    "UIAspectRatioConstraint", "UISizeConstraint", "UIStroke", "UIGradient",
    "UIScale", "UIFlexItem", "UIPageLayout", "BillboardGui", "SurfaceGui",
    "ViewportFrame",
    # Constraints / physics
    "Constraint", "WeldConstraint", "Motor6D", "AlignPosition",
    "AlignOrientation", "LinearVelocity", "AngularVelocity", "VectorForce",
    "Attachment", "RodConstraint", "RopeConstraint", "SpringConstraint",
    "HingeConstraint", "PrismaticConstraint", "BodyVelocity", "BodyPosition",
    # Misc heavy hitters
    "TweenInfo", "Terrain", "Seat", "VehicleSeat", "SpawnLocation",
]

# Curated datatypes whose constructors/members are most-used.
CURATED_DATATYPES = [
    "Vector3", "Vector2", "CFrame", "Color3", "UDim", "UDim2", "Ray",
    "Region3", "Rect", "TweenInfo", "Instance", "Enum", "NumberRange",
    "NumberSequence", "ColorSequence", "BrickColor", "Random", "RaycastParams",
    "OverlapParams", "PhysicalProperties", "Font",
]

SKIP_TAGS = {"Deprecated", "NotScriptable"}
SEC_NONE = ("None", None)


def is_public(member):
    tags = set(member.get("Tags") or [])
    if tags & SKIP_TAGS:
        return False
    sec = member.get("Security")
    if isinstance(sec, dict):
        if sec.get("Read") not in SEC_NONE and sec.get("Write") not in SEC_NONE:
            # both sides gated -> internal
            if sec.get("Read") not in SEC_NONE and sec.get("Write") not in SEC_NONE:
                return False
    elif sec not in SEC_NONE:
        return False
    return True


def type_str(vt):
    if not isinstance(vt, dict):
        return "?"
    return vt.get("Name", "?")


def fmt_member(m):
    mt = m["MemberType"]
    name = m["Name"]
    if mt == "Property":
        return f"  .{name}: {type_str(m.get('ValueType'))}"
    if mt == "Function":
        params = ", ".join(
            f"{p.get('Name','_')}: {type_str(p.get('Type'))}" for p in m.get("Parameters", [])
        )
        ret = type_str(m.get("ReturnType")) if isinstance(m.get("ReturnType"), dict) else "()"
        return f"  :{name}({params}) -> {ret}"
    if mt == "Event":
        params = ", ".join(
            f"{p.get('Name','_')}: {type_str(p.get('Type'))}" for p in m.get("Parameters", [])
        )
        return f"  .{name}: Event({params})"
    if mt == "Callback":
        return f"  .{name}: Callback"
    return f"  {name}"


def main():
    if not os.path.exists(DUMP):
        sys.exit(f"API dump not found at {DUMP}. Run scripts/update_docs.sh first.")
    d = json.load(open(DUMP))
    by_name = {c["Name"]: c for c in d["Classes"]}
    services = sorted(c["Name"] for c in d["Classes"] if "Service" in (c.get("Tags") or []))

    out = []
    out.append("# Roblox Engine API Cheat-Sheet (generated)\n")
    out.append(f"Engine classes: {len(d['Classes'])} · enums: {len(d['Enums'])} · "
               f"generated from API-Dump.json.\n")
    out.append("> This lists concrete member signatures for the **highest-traffic** APIs only. "
               "For any other API, use the indexes in `api/engine-api-index.txt` (one-liners for "
               "every class/enum/datatype) and WebFetch "
               "`https://create.roblox.com/docs/reference/engine/classes/<Name>.md`.\n")
    out.append("Signature legend: `.prop: Type` · `:method(args) -> Ret` · `.Event: Event(args)`. "
               "Deprecated & non-scriptable members are omitted.\n")

    out.append("\n## All Services (319)\n")
    out.append("`game:GetService(\"Name\")` for any of these:\n")
    # wrap services into lines
    line = ""
    for s in services:
        if len(line) + len(s) + 2 > 100:
            out.append(line)
            line = ""
        line += s + ", "
    if line:
        out.append(line.rstrip(", "))

    out.append("\n## Curated class members\n")
    for cname in CURATED:
        c = by_name.get(cname)
        if not c:
            continue
        sup = c.get("Superclass", "")
        out.append(f"\n### {cname}" + (f"  ‹{sup}›" if sup and sup != "<<<ROOT>>>" else ""))
        members = [m for m in c.get("Members", []) if is_public(m)]
        props = [m for m in members if m["MemberType"] == "Property"]
        funcs = [m for m in members if m["MemberType"] == "Function"]
        events = [m for m in members if m["MemberType"] == "Event"]
        cbs = [m for m in members if m["MemberType"] == "Callback"]
        block = []
        for group in (props, funcs, events, cbs):
            for m in sorted(group, key=lambda x: x["Name"]):
                block.append(fmt_member(m))
        if block:
            out.append("```")
            out.extend(block)
            out.append("```")
        else:
            out.append("_(inherits all members from superclass)_")

    # Datatypes
    out.append("\n## Curated datatypes\n")
    dt_by_name = {t["Name"]: t for t in d.get("DataTypes", d.get("Datatypes", []))} if (
        "DataTypes" in d or "Datatypes" in d) else {}
    if dt_by_name:
        for tname in CURATED_DATATYPES:
            t = dt_by_name.get(tname)
            if not t:
                continue
            out.append(f"\n### {tname}")
            block = [fmt_member(m) for m in t.get("Members", []) if is_public(m)]
            if block:
                out.append("```")
                out.extend(block[:60])
                out.append("```")
    else:
        out.append("_(datatype members not present in this dump; see "
                   "`api/engine-api-index.txt` datatype section and WebFetch the .md pages)_")

    with open(OUT, "w") as f:
        f.write("\n".join(out) + "\n")
    print(f"Wrote {OUT} ({os.path.getsize(OUT)//1024} KB, {len(out)} lines)")


if __name__ == "__main__":
    main()
