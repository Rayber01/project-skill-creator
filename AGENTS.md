# AGENTS.md

Guidance for AI coding agents working in this repository.

## What this repo is
`project-skill-creator` is an open-source Agent Skill that helps AI agents design, validate and install project-specific skills. The skill itself lives in `skills/project-skill-creator/`; everything else supports distribution and quality.

## Layout
- `skills/project-skill-creator/`: the skill (`SKILL.md`, `references/`, `assets/`, `scripts/`).
- `adapters/`: `install.sh`, `package.sh`, and chat prompts for assistants without skills support.
- `examples/`: validated sample skills and rejected candidates.
- `tests/`: unit tests (standard library `unittest`).
- `.github/`: CI, release workflow and templates.

## Commands
```bash
python3 skills/project-skill-creator/scripts/validate_skill.py --all --strict skills examples
python3 -m unittest discover -s tests -v
bash adapters/package.sh        # builds dist/project-skill-creator.zip
```
Run both checks before proposing a change.

## Conventions
- Skill frontmatter: single-line `description` (max 1024 chars) that says what the skill does and when to use it; `name` equals the folder name.
- Keep `SKILL.md` short; put detail in `references/`.
- Python: standard library only, 3.9+. Shell: bash with `set -euo pipefail`.
- Installation path claims must come from official agent documentation; update the "Last verified" date in `skills/project-skill-creator/references/install-paths.md` when you re-check.
- Never commit secrets, tokens or personal data.
- Update `CHANGELOG.md` for user-visible changes.

## If you are asked to create skills for another project
Read `skills/project-skill-creator/SKILL.md` and follow its workflow.
