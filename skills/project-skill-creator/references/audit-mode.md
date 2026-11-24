# Audit and improve existing skills

Use when the project already has skills, or the user asks to review, clean up or upgrade them.

1. **Inventory**: list every skill folder in `.agents/skills`, `.claude/skills`, `.opencode/skills`, `.gemini/skills` and the global equivalents that apply. Note duplicates (same name in two locations).
2. **Validate**: run `python3 scripts/validate_skill.py --all <skills-dir>` (or the manual checks in `references/no-shell-mode.md`).
3. **Review each skill** against `references/quality-checklist.md`:
   - Does the description say when to use it, with real trigger words?
   - Is the body short, with detail in `references/`?
   - Do referenced commands, paths and tools still exist in the repo?
   - Does it still earn its place? Re-score with `references/decision-tree.md`.
4. **Find overlap**: skills whose descriptions would trigger on the same request. Merge them or sharpen the boundaries with "Do not use for ...".
5. **Propose changes** as a short list: keep / fix / merge / split / remove, one line of reasoning each.
6. **Apply only what the user approves.** Never delete a skill without explicit confirmation. Re-run validation after each change.
7. **Report** what changed and any follow-ups (for example a skill that needs a script review).
