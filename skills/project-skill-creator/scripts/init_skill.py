#!/usr/bin/env python3
"""Create a new skill folder from assets/SKILL.template.md.

Usage:
    init_skill.py NAME --description "What it does. Use when ..." [--dest DIR]
                  [--resources scripts,references,assets] [--force]

Standard library only (Python 3.9+).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_skill import MAX_DESCRIPTION, MAX_NAME, NAME_RE  # noqa: E402

TEMPLATE = Path(__file__).resolve().parent.parent / "assets" / "SKILL.template.md"
RESOURCE_DIRS = {"scripts", "references", "assets"}
DEFAULT_DESCRIPTION = "TODO what this skill does. Use when TODO. Do not use for TODO."


def yaml_scalar(value: str) -> str:
    """Return value as a safe single-line YAML scalar."""
    value = " ".join(value.split())
    if re.search(r": | #|^[-?:,\[\]{}#&*!|>'\"%@`]", value):
        return json.dumps(value, ensure_ascii=False)
    return value


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Scaffold a new Agent Skill.")
    parser.add_argument("name", help="skill name: lowercase kebab-case, max 64 chars")
    parser.add_argument("--description", default=DEFAULT_DESCRIPTION, help="single-line description")
    parser.add_argument("--dest", default=".", help="folder that will contain the new skill folder")
    parser.add_argument("--resources", default="", help="comma list of extra folders: scripts,references,assets")
    parser.add_argument("--force", action="store_true", help="overwrite SKILL.md if the skill already exists")
    args = parser.parse_args(argv)

    if not NAME_RE.match(args.name) or len(args.name) > MAX_NAME:
        print(f"ERROR invalid name '{args.name}': use lowercase letters, digits and single hyphens (max {MAX_NAME})")
        return 1
    description = " ".join(args.description.split())
    if len(description) > MAX_DESCRIPTION:
        print(f"ERROR description is {len(description)} chars (max {MAX_DESCRIPTION})")
        return 1
    resources = [r.strip() for r in args.resources.split(",") if r.strip()]
    unknown = [r for r in resources if r not in RESOURCE_DIRS]
    if unknown:
        print(f"ERROR unknown resource folder(s): {', '.join(unknown)} (allowed: {', '.join(sorted(RESOURCE_DIRS))})")
        return 1
    if not TEMPLATE.is_file():
        print(f"ERROR template not found: {TEMPLATE}")
        return 1

    skill_dir = Path(args.dest).resolve() / args.name
    skill_md = skill_dir / "SKILL.md"
    if skill_md.exists() and not args.force:
        print(f"ERROR {skill_md} already exists (use --force to overwrite)")
        return 1

    text = TEMPLATE.read_text(encoding="utf-8")
    title = args.name.replace("-", " ").title()
    text = (
        text.replace("{{name}}", args.name)
        .replace("{{description}}", yaml_scalar(description))
        .replace("{{title}}", title)
    )
    skill_dir.mkdir(parents=True, exist_ok=True)
    skill_md.write_text(text, encoding="utf-8")
    for resource in resources:
        (skill_dir / resource).mkdir(exist_ok=True)
        (skill_dir / resource / ".gitkeep").touch()

    print(f"Created {skill_md}")
    print("Next: edit the TODOs, then run: python3 scripts/validate_skill.py " + str(skill_dir))
    return 0


if __name__ == "__main__":
    sys.exit(main())
