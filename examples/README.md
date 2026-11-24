# Examples

Three skills of increasing complexity. They are validated in CI, so they double as regression fixtures.

| Example | Shows |
|---|---|
| [`new-react-component`](new-react-component/SKILL.md) | The simplest useful skill: one file, clear trigger, numbered steps |
| [`laravel-migration`](laravel-migration/SKILL.md) | Progressive disclosure: conventions live in `references/` |
| [`release-checklist`](release-checklist/SKILL.md) | A deterministic check in `scripts/`, judgment steps in the body |

## Rejected candidates (what NOT to turn into a skill)

These came up while analyzing sample projects and were filtered out by `references/decision-tree.md` in the skill.

| Candidate | Score | Better home | Why |
|---|---|---|---|
| "Run Prettier before committing" | 2/10 | Git hook or `package.json` script | Deterministic single command; no judgment |
| "Explain how git rebase works" | 1/10 | Nothing | Generic knowledge the model already has |
| "Always use 2-space indentation and named exports" | 3/10 | `AGENTS.md` rule | Applies to every task, not an occasional workflow |
| "Migrate the legacy invoices table (one time)" | 2/10 | A one-off prompt or script | Rare and will never repeat |
| "Review pull requests" (everything about reviewing) | 5/10 | Split into narrow skills | Too broad: several jobs in one |
