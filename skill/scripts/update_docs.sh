#!/usr/bin/env bash
# Refresh the Roblox knowledge base: re-pull docs + API dump + indexes, regenerate cheat-sheet.
# Raw docs land in data/raw/ (gitignored). Committed artifacts: skill/api/*.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
RAW="$ROOT/data/raw"
API="$ROOT/skill/api"
mkdir -p "$RAW" "$API"

echo "==> creator-docs (shallow clone/refresh)"
if [ -d "$RAW/creator-docs/.git" ]; then
  git -C "$RAW/creator-docs" pull --depth 1 --ff-only origin main || \
    git -C "$RAW/creator-docs" fetch --depth 1 origin main
else
  git clone --depth 1 https://github.com/Roblox/creator-docs.git "$RAW/creator-docs"
fi

echo "==> Engine API dump (MaximumADHD/Roblox-Client-Tracker)"
RCT="https://raw.githubusercontent.com/MaximumADHD/Roblox-Client-Tracker/roblox"
curl -fsSL "$RCT/API-Dump.json" -o "$RAW/API-Dump.json"
curl -fsSL "$RCT/version.txt"  -o "$RAW/version.txt" || true

echo "==> Live llms.txt indexes (create.roblox.com)"
curl -fsSL "https://create.roblox.com/docs/reference/engine/llms.txt" -o "$API/engine-api-index.txt"
curl -fsSL "https://create.roblox.com/docs/llms.txt"                   -o "$API/docs-index.txt"
curl -fsSL "https://create.roblox.com/docs/cloud/llms.txt"             -o "$API/cloud-api-index.txt"

echo "==> Regenerate API cheat-sheet from dump"
python3 "$ROOT/skill/scripts/build_api_cheatsheet.py"

# record the engine version these indexes were built from
if [ -f "$RAW/version.txt" ]; then cp "$RAW/version.txt" "$API/STUDIO_VERSION"; fi

echo "==> Done. Engine version: $(cat "$API/STUDIO_VERSION" 2>/dev/null || echo unknown)"
echo "    Committed artifacts updated in skill/api/. Raw docs in data/raw/ (gitignored)."
echo "    Re-run topic distillation only after a major platform change."
