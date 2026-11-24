# Skill format and portability notes

Based on the open Agent Skills specification (https://agentskills.io/specification). Check it for changes; agents add fields over time.

## Folder layout
```
skill-name/
  SKILL.md        required, exactly this name (uppercase)
  scripts/        optional: executable helpers
  references/     optional: docs loaded on demand
  assets/         optional: templates and static files
```

## Frontmatter

| Field | Required | Rules |
|---|---|---|
| `name` | yes | At most 64 chars. Lowercase letters, digits and single hyphens; no leading/trailing hyphen. Must equal the folder name. |
| `description` | yes | 1-1024 chars. What it does and when to use it. |
| `license` | no | License name or reference to a bundled file. |
| `compatibility` | no | At most 500 chars. Environment requirements (tools, network, agents). |
| `metadata` | no | Map of string keys to string values (for example `version`). |
| `allowed-tools` | no | Experimental and agent-specific. Least privilege; see `references/security.md`. |

## Portability rules (what actually breaks across agents)
1. Keep `name` and `description` on a single line. Some agents (Codex, for example) reject multi-line values. Quote the description if it contains `: ` or ` #`.
2. The file must be called `SKILL.md`, in capitals.
3. Names must be unique across every location an agent reads. Avoid installing the same skill in two paths read by one agent.
4. Keep the core instructions agent-neutral. Do not depend on one agent's tools or slash commands; if you need agent-specific behavior, put it in a clearly labelled section or an optional file.
5. Reference bundled files with relative paths from the skill folder (`references/api.md`, `scripts/check.sh`). Agents resolve them against the skill folder, not the current working directory.
6. Do not rely on a shell, network or specific interpreter being present. Say so in `compatibility` when a script needs one.
7. Keep `SKILL.md` under about 500 lines. Move detail to `references/` (progressive disclosure: agents load only name and description up front, the body on activation, references on demand).
8. Optional agent-specific metadata files (for example `agents/openai.yaml` for Codex UI settings) are allowed but must not be required for the skill to work.
