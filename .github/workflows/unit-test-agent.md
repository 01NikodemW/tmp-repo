---
name: Copilot Unit Test Agent
description: Maintain React and FastAPI unit tests for pull request changes.
on:
  pull_request:
    types: [opened, reopened, synchronize]
engine:
  id: copilot
  agent: unit-test-agent
permissions:
  contents: read
  pull-requests: read
  copilot-requests: write
checkout:
  fetch-depth: 0
tools:
  edit:
  bash:
    - git status
    - "git status *"
    - "git diff *"
    - "git show *"
    - "git ls-files *"
    - "npm --prefix frontend ci --ignore-scripts"
    - "npm --prefix frontend test *"
    - "npm --prefix frontend run *"
    - "python -m pip install -r backend/requirements.txt"
    - "python -m pytest *"
    - "pytest *"
runtimes:
  node:
    version: "22"
  python:
    version: "3.12"
network:
  allowed: [defaults, copilot, github, node, python]
safe-outputs:
  push-to-pull-request-branch:
    max: 1
    max-patch-size: 256
    allowed-files:
      - "**/*.test.ts"
      - "**/*.test.tsx"
      - "**/*.spec.ts"
      - "**/*.spec.tsx"
      - "**/test_*.py"
      - "test_*.py"
    github-token-for-extra-empty-commit: none
  add-comment:
    max: 1
max-turns: 35
max-ai-credits: 300
timeout-minutes: 20
---

# Unit tests for this pull request

Use the `unit-test-agent` custom agent and its React and FastAPI skills.
Analyze the changes in this PR against its base branch. Only work on changed
React/TypeScript and Python/FastAPI source files with testable behavior.

For each relevant file, decide whether a test is needed, create or update only
matching test files, and run the focused tests. If dependencies are missing,
install only the declared project dependencies inside the agent sandbox.
For npm use `npm --prefix frontend ci --ignore-scripts`. Do not run package
lifecycle scripts. For Python install only `backend/requirements.txt`.
Never read or expose secrets. Do not change production code or project configuration.

When tests pass, commit only the changed test files on this PR's head branch and
use the `push-to-pull-request-branch` safe output to publish them. Do not push
if any generated test is unverified or failing. The safe output allows only
test-file paths; do not attempt to bypass that restriction.

Add one concise PR comment stating which tests were created or updated, which
source changes were skipped and why, the exact test commands and results, and
any unresolved failures. If no tests are needed, only post the comment.
