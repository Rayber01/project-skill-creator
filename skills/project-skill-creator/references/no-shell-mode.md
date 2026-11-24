# Manual validation (no shell, no Python)

For chat-only environments or sandboxes without Python. Check each item by reading the draft; fix before delivering.

1. The file is named `SKILL.md`, and the folder name equals `name`.
2. The file starts with `---` and the frontmatter closes with `---` on its own line.
3. `name`: lowercase letters, digits, single hyphens; at most 64 chars; no leading/trailing hyphen.
4. `description`: on ONE line, between 1 and 1024 chars, says what it does AND when to use it.
5. If the description contains `: ` or ` #`, it is wrapped in double quotes.
6. Only standard frontmatter fields are used (`name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`).
7. The body is not empty and is under about 500 lines.
8. Every `references/...`, `scripts/...` or `assets/...` path mentioned exists in the deliverable.
9. No TODO placeholders are left.
10. No secrets, tokens, keys or personal data anywhere.

In a chat, deliver the skill as one fenced code block per file, each preceded by its relative path (for example `my-skill/SKILL.md`), so the user can copy them into folders.
