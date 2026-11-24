# Security policy

## Why this matters
Agent Skills are instructions that agents follow and sometimes scripts that run with your permissions. Review any skill (including this one) before installing it, especially files under `scripts/`.

## Supported versions
Only the latest release receives fixes.

## Reporting a vulnerability
Please do not open a public issue for security problems. Use GitHub's private vulnerability reporting: open the repository's **Security** tab and choose **Report a vulnerability**. Include the affected file, steps to reproduce and the impact you see.

You can expect an acknowledgement within a few days. Fixes are released as a patch version and noted in the changelog.

## Scope
- Scripts in this repository (`install.sh`, `package.sh`, `validate_skill.py`, `init_skill.py`).
- Instructions in the skill that could lead an agent to unsafe behavior (for example, overwriting files without confirmation or leaking secrets).
