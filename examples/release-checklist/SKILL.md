---
name: release-checklist
description: Runs the pre-release checks and prepares a tagged release with a changelog entry. Use when the user asks to cut, prepare or publish a release or to bump the version. Do not use for hotfix deploys or for CI configuration changes.
---

# Release checklist

Prepare a release in a repeatable way.

## Steps
1. Run `scripts/preflight.sh` (set `TEST_CMD` to the project's test command). Stop and report if it fails.
2. Ask the user for the new version number if it was not given; follow semantic versioning.
3. Add an entry to `CHANGELOG.md` summarizing commits since the last tag.
4. Bump the version in the project's manifest file.
5. Show the diff and wait for the user's approval.
6. Only after approval, create the commit and the annotated tag. Do not push unless the user asks.

## Done when
- Preflight passed, the changelog and version are updated, and the tag exists locally.
