---
name: fastapi-unit-tests
description: Use when creating or updating pytest unit tests for changed Python services, dependencies, or FastAPI endpoints in a pull request.
---

# FastAPI unit tests

## Inspect

1. Read the changed Python file and PR diff. Find its existing test, nearby fixtures,
   and the relevant application or router setup.
2. Check how the repository runs pytest and whether it uses `TestClient`, `httpx.AsyncClient`,
   async pytest support, dependency overrides, or service-level fixtures.
3. Follow only dependencies needed to understand the changed behavior.

## Plan and write

- Test observable behavior: service return values, HTTP status and response bodies,
  validation, authorization outcomes, errors, and important edge cases.
- Prefer existing fixtures. Override FastAPI dependencies and mock databases or external
  services at their boundaries. Restore overrides and mocks after each test.
- Use the project's established sync or async style. Keep tests deterministic and isolated;
  avoid real network calls, production credentials, and persistent shared state.
- Add tests to the corresponding `test_*.py` file, or create one in the established tests
  location. Reuse parametrization when it makes distinct cases easier to understand.
- Avoid tests that only call a function without checking a meaningful result, and avoid
  brittle assertions on private implementation details.

## Verify

Run targeted pytest for each changed test file. Inspect failures, correct generated tests,
and rerun. If a failure reveals a production defect, report it without editing production
code. State clearly when the test environment prevents verification.
