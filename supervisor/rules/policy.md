# Supervisor Policy (Constitution)

The Supervisor Agent governs automated work in this repository across phases:
**preflight → validate → judge → forecast → gate**.

## Invariants
- Never inline secrets. All secrets must come from environment variables or secret managers.
- Work must remain within the current **size budget** and **allowed paths**.
- All changes must include or update tests. Coverage for touched files should not decrease.
- If a change touches database schema, auth, payments, PII, or crosses multiple domain boundaries,
  the task must be **split** into smaller PRs before proceeding.
- URD/TechSpec acceptance criteria must be traceable to code changes and tests in the PR.
- Each PR must include docs updates (if user-facing), a rollback note, and a feature flag where applicable.

## Verdicts
- **approve** → proceed to the next phase
- **revise** → return to previous phase with Supervisor notes
- **block** → unsafe or ambiguous; requires human clarification

## Merge Gate
A PR can be promoted only if:
1) Lint/typecheck/tests pass and coverage ≥ threshold
2) Dual-model review has no unresolved **must-fix**
3) Supervisor risk score < 0.35 and rollback/flag docs are present

_Last updated: 2025-10-20T17:34:53.456054Z_
