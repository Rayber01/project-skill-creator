#!/usr/bin/env bash
# Pre-release checks: clean git tree, on the release branch, tests pass.
# Usage: TEST_CMD="npm test" RELEASE_BRANCH=main scripts/preflight.sh
set -euo pipefail

BRANCH="${RELEASE_BRANCH:-main}"
TEST_CMD="${TEST_CMD:-}"

[[ -z "$(git status --porcelain)" ]] || { echo "FAIL: working tree is not clean"; exit 1; }
[[ "$(git rev-parse --abbrev-ref HEAD)" == "$BRANCH" ]] || { echo "FAIL: not on branch $BRANCH"; exit 1; }

if [[ -n "$TEST_CMD" ]]; then
  bash -c "$TEST_CMD"
else
  echo "WARN: TEST_CMD is not set; skipping tests"
fi
echo "OK: preflight passed"
