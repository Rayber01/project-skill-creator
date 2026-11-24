# Project Skill Creator

**English** | [Español](README.es.md)

An open, agent-neutral [Agent Skill](https://agentskills.io/specification) that lets AI agents design, validate and install **their own project-specific skills**. Point your agent at a repository, ask for a skill, and it will read the project, decide what deserves to be a skill, draft a correct `SKILL.md`, validate it, give you test prompts and install it in the right place.

Works with opencode, Claude Code, Gemini CLI, Google Antigravity and Codex. For ChatGPT, Gemini and Claude on the web there are ready-to-paste chat prompts.

## Why

- Skills are most useful when they encode **your** project's conventions, but writing good ones is fiddly: a weak `description` means the skill never activates, and every agent looks in a different folder.
- This skill gives any agent a repeatable workflow, a decision tree (skill vs `AGENTS.md` rule vs script vs command vs subagent), a quality checklist and a validator.

## Quick start

```bash
git clone https://github.com/Rayber01/project-skill-creator.git
cd project-skill-creator

# Install into the current project for agents that read .agents/skills (opencode, Codex, Gemini CLI, Antigravity)
bash adapters/install.sh --agent agents --project-dir /path/to/your/project

# Or pick your agent / global scope
bash adapters/install.sh --agent opencode --scope global
bash adapters/install.sh --agent claude --project-dir /path/to/your/project
bash adapters/install.sh --list            # show every target path
```
Then, in your agent: *"Use the project-skill-creator skill to analyze this repo and propose skills for our recurring workflows."*

### Other ways to install
| Where | How |
|---|---|
| Any agent, manually | Copy `skills/project-skill-creator/` into the agent's skills folder (see the table below) |
| Gemini CLI | `gemini skills install https://github.com/Rayber01/project-skill-creator.git` (or `gemini skills link <dir>`) |
| Claude.ai / Claude Desktop | `bash adapters/package.sh`, then upload `dist/project-skill-creator.zip` in the Skills settings |
| ChatGPT, Gemini web, others | Paste [`adapters/chat-prompt.en.md`](adapters/chat-prompt.en.md) as custom instructions, a Gem or a project prompt |

### Where each agent reads skills
| Agent | Project | Global |
|---|---|---|
| opencode | `.opencode/skills/` (also `.claude/skills/`, `.agents/skills/`) | `~/.config/opencode/skills/` |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |
| Gemini CLI | `.gemini/skills/` or `.agents/skills/` | `~/.gemini/skills/` or `~/.agents/skills/` |
| Antigravity | `.agents/skills/` | `~/.gemini/config/skills/` |
| Codex | `.agents/skills/` | `~/.agents/skills/` |

Paths change between versions. The full table, the coverage matrix and official links (last verified 2026-11-24) are in [`references/install-paths.md`](skills/project-skill-creator/references/install-paths.md). Install each skill in **one** location per agent to avoid duplicates.

## What the skill does

1. **Reads the project**: stack, docs, scripts, CI, existing skills.
2. **Filters candidates** with a scored decision tree, and says where each belongs (skill, `AGENTS.md`, script, command, subagent, nothing).
3. **Interviews you** briefly (at most 3 questions) if essentials are missing.
4. **Drafts** `SKILL.md` from a template with a trigger-oriented one-line description and progressive disclosure.
5. **Validates** with `scripts/validate_skill.py`, or a manual checklist when there is no shell.
6. **Gives test prompts**: two that should activate it, one that must not.
7. **Installs** after asking agent and scope, never overwriting without permission.
8. **Audit mode** reviews and improves skills you already have.

## Example prompts
- "Analyze this repo and suggest which of our workflows should become skills."
- "Create a skill for how we write database migrations here."
- "Audit the skills in `.agents/skills` and tell me which to merge or remove."
- "Crea una skill para nuestro proceso de release."

## Validator

```bash
python3 skills/project-skill-creator/scripts/validate_skill.py path/to/skill
python3 skills/project-skill-creator/scripts/validate_skill.py --all --strict skills examples
```
It checks: `SKILL.md` name and case, frontmatter, `name` rules and folder match, single-line `description` (some agents reject multi-line), length limits, internal links, TODO leftovers, duplicate names and likely secrets. Standard library only.

## Repository layout

```
skills/project-skill-creator/   the skill: SKILL.md, references/, assets/, scripts/
adapters/                       install.sh, package.sh, chat prompts (en/es)
examples/                       three validated skills + rejected candidates
tests/                          unit tests
.github/                        CI, release workflow, issue/PR templates
```

## Contributing

Issues and PRs are welcome, especially **agent path updates**, **examples** and **translations**. See [CONTRIBUTING.md](CONTRIBUTING.md). Skills can run code: read [SECURITY.md](SECURITY.md) and review any skill before installing it.

## License

[MIT](LICENSE)
# project-skill-creator
