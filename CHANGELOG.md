# Changelog

All notable changes to this project are documented here. Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow [Semantic Versioning](https://semver.org/).

## [0.1.1] - 2026-11-25
### Fixed
- CI: pin runners (ubuntu-24.04 and ubuntu-26.04), disable fail-fast, update actions to v7 and run on master.
- Validator: redact secret details in console output (code scanning alert #1).

## [0.1.0] - 2026-11-24
### Added
- `project-skill-creator` skill: create, audit and improve project-specific Agent Skills (8-step workflow).
- References: decision tree with scoring, format and portability spec, quality checklist, audit mode, no-shell mode, security notes, installation paths.
- Templates for new skills and test prompts; `init_skill.py` scaffolder.
- `validate_skill.py`: frontmatter, naming, single-line description, link, secret and size checks; `--all` and `--strict` modes.
- `adapters/install.sh` (opencode, Claude Code, Gemini CLI, Antigravity, Codex, universal `.agents`) and `adapters/package.sh` (upload-ready zip).
- Chat prompts (English and Spanish) for assistants without skills support.
- Three validated examples plus a list of rejected candidates.
- Unit tests, CI validation workflow and release workflow.
