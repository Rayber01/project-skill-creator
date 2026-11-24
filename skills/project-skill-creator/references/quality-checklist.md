# Quality checklist

## The description decides everything
The agent sees only `name` and `description` when choosing a skill. Write it as: **what it does + when to use it + phrases the user says + when not to use it.**

Weak:
> Helps with database stuff.

Weak (describes the internals, not the trigger):
> Analyzes the repo, drafts files, validates them and installs them.

Good:
> Creates Laravel database migrations that follow the project naming and safety conventions. Use when the user asks to add, change or drop a table or column. Do not use for seeding data.

Tips:
- Use the words users really say ("add a column", "release", "scaffold a component"), including their language if the team is not English-speaking.
- Name the boundary with a "Do not use for ..." sentence when a neighbouring task exists.
- Aim for 150-400 chars. One line. Third person or imperative, not "I".

## Body checklist
- [ ] Opens with the outcome in one sentence.
- [ ] Numbered, imperative steps; each step is something observable.
- [ ] States "done when" criteria (tests pass, file exists, command output).
- [ ] Defaults instead of menus: pick one approach, mention alternatives only if needed.
- [ ] Under about 500 lines; long material moved to `references/`.
- [ ] Every referenced file exists (the validator checks this).
- [ ] No secrets, tokens, personal data or absolute paths of one machine.
- [ ] Scripts are documented, deterministic and need no network by default.
- [ ] Tested with the three prompts from `assets/test-prompts.template.md`.

## Anti-patterns
- **Kitchen-sink skill**: several jobs in one. Split it.
- **Duplicate of AGENTS.md**: a rule that applies to every task belongs in `AGENTS.md`, not in a skill.
- **Vague trigger**: "Use for coding tasks" activates always or never.
- **Wall of text**: explaining what the model already knows.
- **Hidden dependencies**: needs a tool, env var or network the skill never mentions.
- **Fragile paths**: hardcoded absolute paths or one agent's directories.
- **Untested**: never run against a realistic prompt.
- **Stale facts**: copies of versions, URLs or file lists that will drift; point to the source instead.
