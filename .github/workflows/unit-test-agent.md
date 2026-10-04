---
name: Copilot Unit Test Agent
description: Maintain React and FastAPI unit tests for pull request changes.
on:
  pull_request:
    types: [opened, reopened, synchronize, ready_for_review]
  workflow_dispatch:
    inputs:
      mode:
        description: Analyze PR changes or backfill existing missing coverage
        type: choice
        options: [pr, coverage]
        default: pr
concurrency:
  job-discriminator: "${{ github.run_id }}"
engine:
  id: copilot
  agent: unit-test-agent
permissions:
  contents: read
  pull-requests: read
  copilot-requests: none
skills:
  - .github/skills/pr-test-analysis
  - .github/skills/coverage-backfill
  - .github/skills/react-unit-tests
  - .github/skills/fastapi-unit-tests
checkout:
  fetch-depth: 0
pre-agent-steps:
  # gh-aw v0.89.21 checks the whole PR history against allowed-files.
  # Restrict that check to agent commits using the framework's recorded PR head.
  # Keep the original restrictive behavior when no matching baseline exists.
  - name: Scope file-policy validation to agent commits
    run: |
      node <<'NODE'
      const fs = require('node:fs');
      const path = require('node:path');
      const file = path.join(process.env.RUNNER_TEMP, 'gh-aw/actions/safe_outputs_handlers.cjs');
      const source = fs.readFileSync(file, 'utf8');
      const before = '`origin/${baseBranch}..${pushPinnedSha}`, "--"';
      const after = '`${prHeadBaseline?.sha || `origin/${baseBranch}`}..${pushPinnedSha}`, "--"';
      if (source.split(before).length !== 2) {
        throw new Error('gh-aw policy implementation changed; review the pinned-version workaround');
      }
      fs.writeFileSync(file, source.replace(before, after));
      NODE
tools:
  edit:
  bash:
    - git status
    - "git status *"
    - "git diff *"
    - "git show *"
    - "git rev-parse *"
    - "git merge-base *"
    - "git ls-files *"
    # Copilot CLI matches command identifiers, not shell-style globs.
    # Grant the runtimes needed for dependency installation and test execution.
    - "npm:*"
    - "python:*"
    - "pytest:*"
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
      - "frontend/src/**/*.test.ts"
      - "frontend/src/**/*.test.tsx"
      - "frontend/src/**/*.spec.ts"
      - "frontend/src/**/*.spec.tsx"
      - "backend/tests/**/test_*.py"
    github-token-for-extra-empty-commit: none
  add-comment:
    max: 1
max-turns: 35
max-ai-credits: 300
timeout-minutes: 20
---

# Unit tests for this pull request

Use the `unit-test-agent` custom agent. Read `pr-test-analysis` first, then the
React and/or FastAPI skills for the relevant stack. They are explicitly installed
through `skills:`. Always record the skills actually used in the final report.

Mode: `${{ github.event.inputs.mode || 'pr' }}`.
For `pr`, analyze only testable behavior changed relative to the PR base SHA.
For `coverage`, also read `coverage-backfill` and fill a bounded batch of existing
coverage gaps in the triggering PR. Manual runs MUST provide a PR context via
`aw_context` with `item_type: pull_request` and `item_number`. Without an open,
same-repository PR, do not edit or publish anything; report missing context.

Read base/head SHAs from the PR context or GitHub read tools, verify the checked-out
head, and inspect the three-dot diff. Ignore test-only changes from earlier agent
runs: if no behavioral gap remains, only report why no new tests are needed.

Install only the declared project dependencies inside the sandbox:
`npm --prefix frontend ci` and
`python -m pip install -r backend/requirements.txt`.
Never read/expose secrets or change production code, dependencies or configuration.

Run the relevant baseline before editing. Verify each changed test file and then
run the entire affected stack:

- Frontend: `npm --prefix frontend test`, `npm --prefix frontend run typecheck`.
- Backend: `python -m pytest -c backend/pyproject.toml backend/tests`.

A failed baseline, failing test, failed typecheck or unavailable dependency means
no publication of test changes. Report failures honestly, including commands and
exit status. Repair generated tests at most twice; never modify application code.

When verification passes, inspect the diff, stage only explicit test paths and
commit them on the checked-out PR head. Invoke `push-to-pull-request-branch` for
this triggering PR only. The safe output restricts allowed paths to tests.
Do not directly push, force push, merge, or create another PR.

Use `add-comment` once to report mode, base/head revisions, decisions per file,
created/updated tests, skipped changes and reasons, skills used, exact commands,
counts/results, and unresolved failures. Include the Actions run URL. If tests
are unnecessary or verification is blocked, publish only the report.
If the push tool returns an error, explicitly report that the tests were NOT
published. A successful safe-output response only queues publication; describe
it as queued until the safe-outputs job confirms the remote commit.
