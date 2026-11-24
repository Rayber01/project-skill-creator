#!/usr/bin/env bash
# Install a skill folder into the skills directory of one or more AI agents.
# Keep the path table in sync with skills/project-skill-creator/references/install-paths.md
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SKILL_SRC="$REPO_ROOT/skills/project-skill-creator"
VALIDATOR="$REPO_ROOT/skills/project-skill-creator/scripts/validate_skill.py"
AGENTS_LIST="agents"
SCOPE="project"
PROJECT_DIR="$PWD"
MODE="copy"
FORCE=0
DRY=0
VALIDATE=1
LIST=0

usage() {
  cat <<'USAGE'
Usage: adapters/install.sh [options]

Options:
  -a, --agent LIST       Comma-separated targets (default: agents).
                         agents | opencode | claude | gemini | antigravity | codex
  -s, --scope SCOPE      project (default) or global
  -p, --project-dir DIR  Project root for project scope (default: current directory)
      --skill PATH       Skill folder to install (default: skills/project-skill-creator)
      --link             Symlink instead of copying
  -f, --force            Replace an existing installation
  -n, --dry-run          Print what would happen, change nothing
      --no-validate      Skip validation before installing
  -l, --list             Show the target folder of every agent for the chosen scope
  -h, --help             Show this help

Examples:
  adapters/install.sh --agent opencode --scope global
  adapters/install.sh --agent agents --project-dir ~/code/my-app
  adapters/install.sh --skill ./my-new-skill --agent claude,agents --dry-run

Install each skill in ONE location per agent. See
skills/project-skill-creator/references/install-paths.md for which agent reads which folder.
USAGE
}

die() { echo "error: $*" >&2; exit 1; }

target_base() { # agent scope
  case "$1:$2" in
    agents:project|codex:project|antigravity:project) echo "$PROJECT_DIR/.agents/skills" ;;
    agents:global|codex:global) echo "$HOME/.agents/skills" ;;
    antigravity:global) echo "$HOME/.gemini/config/skills" ;;
    opencode:project) echo "$PROJECT_DIR/.opencode/skills" ;;
    opencode:global) echo "${XDG_CONFIG_HOME:-$HOME/.config}/opencode/skills" ;;
    claude:project) echo "$PROJECT_DIR/.claude/skills" ;;
    claude:global) echo "$HOME/.claude/skills" ;;
    gemini:project) echo "$PROJECT_DIR/.gemini/skills" ;;
    gemini:global) echo "$HOME/.gemini/skills" ;;
    *) return 1 ;;
  esac
}

run() {
  if [[ $DRY -eq 1 ]]; then echo "[dry-run] $*"; else "$@"; fi
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    -a|--agent) [[ $# -ge 2 ]] || die "$1 needs a value"; AGENTS_LIST="$2"; shift 2 ;;
    -s|--scope) [[ $# -ge 2 ]] || die "$1 needs a value"; SCOPE="$2"; shift 2 ;;
    -p|--project-dir) [[ $# -ge 2 ]] || die "$1 needs a value"; PROJECT_DIR="$2"; shift 2 ;;
    --skill) [[ $# -ge 2 ]] || die "$1 needs a value"; SKILL_SRC="$2"; shift 2 ;;
    --link) MODE="link"; shift ;;
    -f|--force) FORCE=1; shift ;;
    -n|--dry-run) DRY=1; shift ;;
    --no-validate) VALIDATE=0; shift ;;
    -l|--list) LIST=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) usage >&2; die "unknown option: $1" ;;
  esac
done

[[ "$SCOPE" == "project" || "$SCOPE" == "global" ]] || die "scope must be 'project' or 'global'"
if [[ "$SCOPE" == "project" ]]; then
  [[ -d "$PROJECT_DIR" ]] || die "project directory not found: $PROJECT_DIR"
  PROJECT_DIR="$(cd "$PROJECT_DIR" && pwd)"
fi

if [[ $LIST -eq 1 ]]; then
  for a in agents opencode claude gemini antigravity codex; do
    printf '%-12s %s\n' "$a" "$(target_base "$a" "$SCOPE")"
  done
  exit 0
fi

[[ -d "$SKILL_SRC" ]] || die "skill folder not found: $SKILL_SRC"
SKILL_SRC="$(cd "$SKILL_SRC" && pwd)"
[[ -f "$SKILL_SRC/SKILL.md" ]] || die "SKILL.md not found in $SKILL_SRC"
name="$(basename "$SKILL_SRC")"

if [[ $VALIDATE -eq 1 ]] && command -v python3 >/dev/null 2>&1 && [[ -f "$VALIDATOR" ]]; then
  python3 "$VALIDATOR" "$SKILL_SRC" || die "validation failed (use --no-validate to skip)"
fi

done_targets=""
IFS=',' read -r -a agent_arr <<< "$AGENTS_LIST"
for agent in "${agent_arr[@]}"; do
  base="$(target_base "$agent" "$SCOPE")" || die "unsupported agent '$agent' (see --help)"
  dest="$base/$name"
  if printf '%s\n' "$done_targets" | grep -Fxq "$dest"; then
    echo "skip    $agent -> $dest (same folder already handled)"
    continue
  fi
  done_targets+="$dest"$'\n'

  if [[ -e "$dest" || -L "$dest" ]]; then
    if [[ $FORCE -eq 1 ]]; then
      [[ -n "$name" && "$(basename "$dest")" == "$name" ]] || die "refusing to remove unexpected path: $dest"
      run rm -rf -- "$dest"
    else
      echo "exists  $agent -> $dest (use --force to replace)"
      continue
    fi
  fi

  run mkdir -p "$base"
  if [[ "$MODE" == "link" ]]; then
    run ln -s "$SKILL_SRC" "$dest"
  else
    run cp -R "$SKILL_SRC" "$dest"
    run find "$dest" -name __pycache__ -type d -prune -exec rm -rf {} +
  fi
  if [[ $DRY -eq 1 ]]; then echo "would install $agent -> $dest ($MODE)"; else echo "install $agent -> $dest ($MODE)"; fi
done

echo "Done. Restart or reload your agent if it does not show the skill (Gemini CLI: /skills reload)."
