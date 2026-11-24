#!/usr/bin/env python3
"""Validate Agent Skills (folders with a SKILL.md) for portability across AI agents.

Usage:
    validate_skill.py PATH [PATH ...]       each PATH is a skill folder
    validate_skill.py --all DIR [DIR ...]   scan DIRs recursively for skills
    validate_skill.py --strict ...          treat warnings as errors

Exit code: 0 = all skills valid, 1 = at least one error (or warning with --strict).
Standard library only (Python 3.9+).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
KEY_RE = re.compile(r"^([A-Za-z0-9_-]+):[ \t]*(.*)$")
BLOCK_SCALAR_RE = re.compile(r"^[>|][+-]?\d?$")
TRIGGER_RE = re.compile(
    r"\b(use when|use this|use it|use for|when the user|when you|triggers?|invoke|"
    r"cuando|usa|úsala|úsalo|utiliza)\b",
    re.IGNORECASE,
)

MAX_NAME = 64
MAX_DESCRIPTION = 1024
MAX_COMPATIBILITY = 500
MAX_BODY_LINES = 500
MIN_DESCRIPTION = 40
KNOWN_KEYS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist"}

SECRET_PATTERNS = [
    ("AWS access key", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("GitHub token", re.compile(r"gh[pousr]_[A-Za-z0-9]{36,}")),
    ("API key (sk-)", re.compile(r"(?<![A-Za-z0-9])sk-[A-Za-z0-9_-]{20,}")),
    ("Slack token", re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}")),
    ("Google API key", re.compile(r"AIza[0-9A-Za-z_-]{35}")),
    ("Private key block", re.compile("-----BEGIN " + r"(?:[A-Z]+ )?PRIVATE KEY-----")),
]

Fields = Dict[str, Tuple[str, str]]  # key -> (text, kind)


def unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] == '"':
        try:
            return str(json.loads(value))
        except ValueError:
            return value[1:-1]
    if len(value) >= 2 and value[0] == value[-1] == "'":
        return value[1:-1].replace("''", "'")
    return re.sub(r"\s+#.*$", "", value)


def split_frontmatter(text: str) -> Optional[Tuple[str, str]]:
    text = text.lstrip("\ufeff").replace("\r\n", "\n").replace("\r", "\n")
    match = re.match(r"^---[ \t]*\n(.*?)\n---[ \t]*(?:\n(.*))?$", text, re.DOTALL)
    if not match:
        return None
    return match.group(1), match.group(2) or ""


def parse_frontmatter(block: str) -> Fields:
    """Tiny YAML subset: top-level keys, scalars, quoted strings, block scalars, maps.

    kind is one of: scalar, block (> or |), multiline (plain scalar continued on
    indented lines), map (nested keys, e.g. metadata).
    """
    fields: Fields = {}
    lines = block.split("\n")
    i = 0
    while i < len(lines):
        match = KEY_RE.match(lines[i])
        if not match:
            i += 1
            continue
        key, value = match.group(1), match.group(2).strip()
        j = i + 1
        cont: List[str] = []
        while j < len(lines) and (lines[j].startswith((" ", "\t")) or not lines[j].strip()):
            cont.append(lines[j])
            j += 1
        indented = [c.strip() for c in cont if c.strip()]
        if BLOCK_SCALAR_RE.match(value):
            fields[key] = (" ".join(indented), "block")
        elif value == "":
            fields[key] = ("", "map" if indented else "scalar")
        elif indented:
            fields[key] = (" ".join([unquote(value)] + indented), "multiline")
        else:
            fields[key] = (unquote(value), "scalar")
        i = j
    return fields


def check_single_line(label: str, text: str, kind: str, errors: List[str]) -> None:
    if kind in ("block", "multiline", "map"):
        errors.append(
            f"frontmatter: '{label}' must be a single-line string "
            "(multi-line values are rejected by some agents, e.g. Codex)"
        )


def check_links(skill_dir: Path, body: str, errors: List[str]) -> None:
    stripped = re.sub(r"```.*?```", "", body, flags=re.DOTALL)
    candidates = set(re.findall(r"\]\(([^)\s#]+)(?:#[^)]*)?\)", stripped))
    for span in re.findall(r"`([^`\n]+)`", stripped):
        if re.match(r"^(?:references|scripts|assets)/[\w.\-/]+$", span):
            candidates.add(span)
    for cand in sorted(candidates):
        if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", cand):  # http:, mailto:, ...
            continue
        if any(ch in cand for ch in "<>*{}$"):  # placeholders such as references/<topic>.md
            continue
        target = (skill_dir / cand).resolve()
        try:
            target.relative_to(skill_dir)
        except ValueError:
            errors.append(f"link points outside the skill folder: {cand}")
            continue
        if not target.exists():
            errors.append(f"broken internal link: {cand}")


def scan_secrets(skill_dir: Path, errors: List[str]) -> None:
    for dirpath, dirnames, filenames in os.walk(skill_dir):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for filename in filenames:
            path = Path(dirpath) / filename
            try:
                if path.stat().st_size > 1_000_000:
                    continue
                data = path.read_bytes()
            except OSError:
                continue
            if b"\x00" in data:
                continue
            for lineno, line in enumerate(data.decode("utf-8", errors="ignore").splitlines(), 1):
                for label, pattern in SECRET_PATTERNS:
                    if pattern.search(line):
                        rel = path.relative_to(skill_dir)
                        errors.append(f"possible secret ({label}) in {rel}:{lineno}")


def validate_skill(skill_dir: Path) -> Tuple[List[str], List[str], Optional[str]]:
    """Return (errors, warnings, skill_name)."""
    errors: List[str] = []
    warnings: List[str] = []
    skill_dir = skill_dir.resolve()
    if not skill_dir.is_dir():
        return [f"not a directory: {skill_dir}"], warnings, None

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        variants = [p.name for p in skill_dir.iterdir() if p.name.lower() == "skill.md"]
        if variants:
            errors.append(f"file must be named exactly SKILL.md (found {variants[0]})")
        else:
            errors.append("SKILL.md not found")
        return errors, warnings, None

    try:
        text = skill_md.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return ["SKILL.md is not valid UTF-8"], warnings, None

    parts = split_frontmatter(text)
    if parts is None:
        return ["missing or malformed YAML frontmatter (must start with --- and end with ---)"], warnings, None
    block, body = parts
    fields = parse_frontmatter(block)

    # name
    name, kind = fields.get("name", ("", "missing"))
    if kind == "missing" or not name:
        errors.append("frontmatter: 'name' is required")
        name = None
    else:
        check_single_line("name", name, kind, errors)
        if len(name) > MAX_NAME:
            errors.append(f"name is {len(name)} chars (max {MAX_NAME})")
        if not NAME_RE.match(name):
            errors.append(
                f"name '{name}' must use lowercase letters, digits and single hyphens "
                "(no leading/trailing hyphen)"
            )
        if name != skill_dir.name:
            errors.append(f"name '{name}' must match the folder name '{skill_dir.name}'")

    # description
    desc, kind = fields.get("description", ("", "missing"))
    if kind == "missing" or not desc:
        errors.append("frontmatter: 'description' is required")
    else:
        check_single_line("description", desc, kind, errors)
        if len(desc) > MAX_DESCRIPTION:
            errors.append(f"description is {len(desc)} chars (max {MAX_DESCRIPTION})")
        if len(desc) < MIN_DESCRIPTION:
            warnings.append("description is very short; say what the skill does and when to use it")
        if not TRIGGER_RE.search(desc):
            warnings.append("description should say WHEN to use the skill (e.g. 'Use when ...')")

    # optional fields
    compat, kind = fields.get("compatibility", ("", "missing"))
    if kind != "missing" and len(compat) > MAX_COMPATIBILITY:
        errors.append(f"compatibility is {len(compat)} chars (max {MAX_COMPATIBILITY})")
    for key in fields:
        if key not in KNOWN_KEYS:
            warnings.append(f"unknown frontmatter field '{key}' (standard fields: {', '.join(sorted(KNOWN_KEYS))})")

    # body
    if not body.strip():
        errors.append("SKILL.md body is empty")
    else:
        line_count = len(body.strip().splitlines())
        if line_count > MAX_BODY_LINES:
            warnings.append(f"body has {line_count} lines (recommended max {MAX_BODY_LINES}); move detail to references/")
    if re.search(r"\bTODO\b", text):
        warnings.append("SKILL.md still contains TODO placeholders")

    check_links(skill_dir, body, errors)
    scan_secrets(skill_dir, errors)
    return errors, warnings, name


def find_skill_dirs(root: Path) -> List[Path]:
    found: List[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        if any(f.lower() == "skill.md" for f in filenames):
            found.append(Path(dirpath))
    return found


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Validate Agent Skills (SKILL.md folders).")
    parser.add_argument("paths", nargs="*", default=["."], help="skill folder(s), or folders to scan with --all")
    parser.add_argument("--all", action="store_true", help="scan the given folders recursively for skills")
    parser.add_argument("--strict", action="store_true", help="treat warnings as errors")
    args = parser.parse_args(argv)

    skill_dirs: List[Path] = []
    for raw in args.paths:
        path = Path(raw)
        if path.is_file() and path.name == "SKILL.md":
            path = path.parent
        if args.all:
            skill_dirs.extend(find_skill_dirs(path))
        else:
            skill_dirs.append(path)
    if not skill_dirs:
        print("ERROR no skills found", file=sys.stderr)
        return 1

    failed = 0
    seen: Dict[str, Path] = {}
    for skill_dir in skill_dirs:
        errors, warnings, name = validate_skill(skill_dir)
        if name:
            if name in seen and seen[name] != skill_dir.resolve():
                errors.append(f"duplicate skill name '{name}' (also in {seen[name]})")
            seen.setdefault(name, skill_dir.resolve())
        label = name or skill_dir.resolve().name
        ok = not errors and not (args.strict and warnings)
        print(f"{'OK   ' if ok else 'FAIL '} {label}  ({skill_dir})")
        for message in errors:
            print(f"  ERROR {message}")
        for message in warnings:
            print(f"  WARN  {message}")
        if not ok:
            failed += 1

    total = len(skill_dirs)
    print(f"\n{total - failed}/{total} skills passed" + (" (strict)" if args.strict else ""))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
