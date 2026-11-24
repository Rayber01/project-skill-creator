# Contributing

Thanks for helping. This project aims to stay small, portable across agents, and correct.

## Setup
No dependencies beyond Python 3.9+ and bash.
```bash
python3 skills/project-skill-creator/scripts/validate_skill.py --all --strict skills examples
python3 -m unittest discover -s tests -v
```
Both must pass before you open a pull request (CI runs the same commands).

## What to contribute
- **Agent support**: new or changed install paths. Update `skills/project-skill-creator/references/install-paths.md` (with the official doc link and the verification date), `adapters/install.sh` and a test in `tests/test_validate_skill.py`.
- **Examples**: a realistic skill under `examples/<name>/` with a trigger-oriented description. Examples must pass `--strict`.
- **Rejected candidates**: add rows to `examples/README.md` with the score and the better home.
- **Validator checks**: add a test for every new check, for both the failing and the passing case.
- **Translations**: keep `README.md` and `README.es.md` in sync; new languages are welcome as `README.<lang>.md`.

## Skill style rules
1. `description` on one line, says what and when, includes real trigger phrases, max 1024 chars.
2. `SKILL.md` under about 500 lines; heavy content in `references/`.
3. Agent-neutral core instructions. Agent-specific details go in clearly labelled sections or optional files.
4. No secrets, tokens, personal data or machine-specific absolute paths.

## Pull requests
- One topic per PR; explain the why.
- Update `CHANGELOG.md` for user-visible changes.
- If you claim an agent behaves a certain way, link the official documentation.

## Security
Report vulnerabilities privately; see [SECURITY.md](SECURITY.md).
