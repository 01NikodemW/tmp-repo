---
name: coverage-backfill
description: Select existing untested frontend and backend behavior from coverage reports for an explicitly requested backfill task.
---

# Backfill existing coverage

Use only when a user explicitly requests missing coverage or workflow mode is
`coverage`. This mode may select unchanged source files; normal PR mode may not.

1. Run `npm --prefix frontend run test:coverage` and
   `python -m pytest -c backend/pyproject.toml backend/tests --cov=backend/app --cov-config=backend/pyproject.toml --cov-report=term-missing --cov-report=json:backend/coverage/coverage.json`.
2. Read `frontend/coverage/coverage-summary.json` and
   `backend/coverage/coverage.json`. Select up to three modules per stack with
   uncovered business behavior, prioritizing HTTP errors, state transitions,
   resource cleanup and validation. Exclude design-system, types, constants,
   declarative schemas/models and entrypoints according to project coverage
   configuration. Do not introduce a global coverage threshold or distribution
   enforcement script.
3. Explain the selected behaviors and what remains outside this batch. Load the
   matching stack skill and write meaningful tests. Avoid pursuing a percentage
   by asserting implementation details or testing trivial constants.
4. Run focused tests, full suites and frontend typecheck. Rerun coverage and report
   the measured before/after values, including any remaining uncovered branches.
   Follow `pr-test-analysis` for PR publication. For a local task, leave a
   reviewable test diff and report instead of pushing or commenting externally.
