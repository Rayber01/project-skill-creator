# Installation paths by agent

Last verified: 2026-11-24 against each vendor's documentation. Agents change these paths; if something does not load, check the official docs listed at the end and restart or reload the agent.

Each skill goes in its own folder: `<skills-dir>/<skill-name>/SKILL.md`.

| Agent | Project scope | Global scope | Notes |
|---|---|---|---|
| Universal (`.agents`) | `<project>/.agents/skills/` | `~/.agents/skills/` | Read by opencode, Codex and Gemini CLI. Antigravity reads the project path only. Claude Code does not read it. |
| opencode | `.opencode/skills/` | `~/.config/opencode/skills/` | Also reads `.claude/skills/` and `.agents/skills/` (project and global). |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` | Also read by opencode. |
| Gemini CLI | `.gemini/skills/` (alias `.agents/skills/`) | `~/.gemini/skills/` (alias `~/.agents/skills/`) | `gemini skills install <git-url-or-path>` and `gemini skills link <dir>` also work. Use `/skills reload`. |
| Antigravity | `.agents/skills/` | IDE: `~/.gemini/config/skills/` (legacy `~/.gemini/antigravity/skills/`). CLI: `~/.gemini/antigravity-cli/skills/` | Docs differ between IDE and CLI versions; check the Customizations panel. |
| Codex (CLI, IDE, app) | `.agents/skills/` (scanned from the working directory up to the repo root) | `~/.agents/skills/` | Older docs mention `.codex/skills/` and `~/.codex/skills/`. Admin scope: `/etc/codex/skills`. Restart Codex after adding skills. |
| Claude.ai / Claude Desktop | n/a | Upload a zip of the skill folder in the Skills settings | Zip so the skill folder is at the root of the archive. |
| ChatGPT | n/a | Skills are supported in ChatGPT; follow OpenAI's current instructions to add one | If unavailable on your plan, use the chat prompt from the repository (`adapters/`). |
| Gemini web and other chat-only tools | n/a | No skills support | Use the chat prompt from the repository as a Gem or custom instructions. |

## Which single location covers which agents?

| Path | opencode | Claude Code | Gemini CLI | Codex | Antigravity |
|---|---|---|---|---|---|
| `.agents/skills/` (project) | yes | no | yes | yes | yes |
| `.claude/skills/` (project) | yes | yes | no | no | no |
| `~/.agents/skills/` (global) | yes | no | yes | yes | no |
| `~/.claude/skills/` (global) | yes | yes | no | no | no |

Pick one location per agent. If you use Claude Code together with Gemini, Codex or Antigravity, you need `.claude/skills/` and `.agents/skills/`; consider a symlink so there is one source of truth, and expect opencode to see both.

## Official docs
- opencode: https://opencode.ai/docs/skills
- Gemini CLI: https://geminicli.com/docs/cli/skills/
- Antigravity: https://antigravity.google/docs/skills
- Codex: https://developers.openai.com/codex/skills
- Agent Skills spec: https://agentskills.io/specification
