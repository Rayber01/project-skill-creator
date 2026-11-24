# Decision tree: skill or something else?

Not everything deserves a skill. A bloated skill library hurts: every description is loaded into the agent's context, and overlapping skills confuse activation.

## 1. Where does the knowledge belong?

| If it is... | Put it in... |
|---|---|
| A short rule that applies to almost every task (style, forbidden actions, how to run tests) | `AGENTS.md` (or `CLAUDE.md` / `GEMINI.md`) |
| Fully deterministic, no judgment needed, one command | A script, Makefile target, npm script or git hook |
| Multi-step, needs judgment, project-specific, needed only sometimes | **A skill** |
| A prompt the user triggers manually with arguments | A custom/slash command (many agents also expose skills as commands) |
| Work that needs isolated context, different permissions or parallelism | A subagent |
| Large reference material consulted rarely | A docs file, plus a pointer from `AGENTS.md` or from the `references/` folder of an existing skill |
| Generic knowledge the model already has | Nothing |

## 2. Score a skill candidate (0-2 each)

| Criterion | 0 | 1 | 2 |
|---|---|---|---|
| Frequency | One-off | A few times per month | Weekly or more |
| Steps | 1 step | 2-3 steps | 4-10 steps with order that matters |
| Project specificity | Generic practice | Some local conventions | Strict local rules, formats or contracts |
| Judgment needed | None (script it) | Some | Substantial (choices, tradeoffs) |
| Cost of getting it wrong | Trivial | Rework | Broken build, data loss, bad release |

- **8-10**: strong candidate, create the skill.
- **5-7**: create it if the user insists, or start with an `AGENTS.md` rule and promote it later.
- **0-4**: do not create a skill.

The thresholds are heuristics. Explain the score in one line instead of hiding behind the number.

## 3. Before creating, check
- Does an existing skill already cover most of it? Extend that one.
- Can it be one skill with a clear job, or is it really two? Split by job, not by size.
- Would a teammate recognize the trigger phrase? If not, the description will be hard to write.

## 4. Reporting
For each candidate give: name, destination (skill / rule / script / ...), score, one-line reason.
