#!/usr/bin/env bash
# Build an upload-ready zip of a skill folder (the folder itself is the zip root).
# Usage: adapters/package.sh [skill-folder] [output-dir]
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SRC="${1:-$REPO_ROOT/skills/project-skill-creator}"
OUT="${2:-$REPO_ROOT/dist}"

[[ -f "$SRC/SKILL.md" ]] || { echo "error: SKILL.md not found in $SRC" >&2; exit 1; }
SRC="$(cd "$SRC" && pwd)"
mkdir -p "$OUT"
OUT="$(cd "$OUT" && pwd)"
name="$(basename "$SRC")"
zipfile="$OUT/$name.zip"

python3 "$REPO_ROOT/skills/project-skill-creator/scripts/validate_skill.py" --strict "$SRC"
rm -f "$zipfile"

if command -v zip >/dev/null 2>&1; then
  (cd "$(dirname "$SRC")" && zip -qr "$zipfile" "$name" -x '*/__pycache__/*' -x '*.pyc' -x '*/.DS_Store')
else
  python3 - "$SRC" "$zipfile" <<'PY'
import os, sys, zipfile
src, out = sys.argv[1], sys.argv[2]
root = os.path.dirname(src)
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
    for dirpath, dirnames, filenames in os.walk(src):
        dirnames[:] = [d for d in dirnames if d != "__pycache__"]
        for fn in filenames:
            if fn.endswith(".pyc") or fn == ".DS_Store":
                continue
            full = os.path.join(dirpath, fn)
            zf.write(full, os.path.relpath(full, root))
PY
fi
echo "Created $zipfile"
