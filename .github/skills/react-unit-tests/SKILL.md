---
name: react-unit-tests
description: Use when creating or updating unit tests for changed React components, hooks, or TypeScript frontend behavior in a pull request.
---

# React unit tests

## Inspect

1. Read the changed component, hook, or module and its PR diff.
2. Find a corresponding test and one nearby representative test. Check `package.json`
   for the actual test runner and scripts. Use the repository's Vitest or Jest conventions.
3. Follow only the imports needed for the changed behavior. Avoid loading the whole frontend.

## Plan and write

- Test behavior visible to a user or caller: rendered states, interactions, callbacks,
  validation, asynchronous results, and error states.
- Prefer React Testing Library queries by role, label, and visible text. Use `userEvent`
  for interactions and `findBy*` or `waitFor` for asynchronous behavior when those tools
  are already available in the project.
- Cover important branches and edge cases introduced by the change. Keep assertions tied
  to outcomes, not component internals or implementation details.
- Mock external boundaries such as HTTP clients, timers, and browser APIs only where needed.
  Reset mocks and cleanup according to the repository's conventions.
- Update an existing test when it already covers the behavior; otherwise create a focused
  `*.test.ts[x]` or `*.spec.ts[x]` beside the source or in the established test directory.
- Avoid trivial render-only tests, broad snapshots, arbitrary sleeps, and assertions that
  merely repeat the implementation.

## Verify

Run the repository's targeted test command for the changed test file. If available, also
run its TypeScript check when new tests introduce typing risk. On failure, inspect the
assertion or setup, fix the test, and rerun it. Report any production behavior that remains
inconsistent instead of editing production code.

## Repository commands and mocks

- Install: `npm --prefix frontend ci`.
- Focused: `npm --prefix frontend test -- src/PATH.test.tsx` (or `.test.ts`).
- Final: `npm --prefix frontend test` and `npm --prefix frontend run typecheck`.
- Coverage: `npm --prefix frontend run test:coverage`.
- In application component tests use the shared design-system mocks:
  `vi.mock('RELATIVE/design-system', () => import('RELATIVE/design-system/mocks'))`.
  Match the source import path; do not duplicate component mock implementations.
- Use real React Query clients with retries disabled when testing cache behavior;
  mock HTTP/API boundaries and clear each client after the test.
