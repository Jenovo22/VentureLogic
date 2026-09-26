# Feature: Typo-Tolerant Password Retrieval

## Objective

Recognize the common `reestablec…` spelling variant as `restablec…` for retrieval without changing the protected lexical retriever or the original question returned to the user.

## Problem and Why

The intent classifier correctly returns `cuenta` for both spellings, but lexical retrieval scores `restablezco` at `0.566` and `reestablezco` at `0.234`. The typo therefore changes the final result from `DUDOSO` to `SIN_EVIDENCIA` even though user intent is unchanged.

## Scope

- Normalize the targeted spelling variant only in the query passed to retrieval.
- Preserve the original question in API/UI output.
- Add regression coverage for spelling, case, and unchanged canonical behavior.
- Do not modify `shared/retriever.py`, protected fixtures, thresholds, dependencies, or the archived assessment artifacts.

## Authorized Scope

- `starter_kit/starter_kit/app.py`
- `starter_kit/starter_kit/tests/test_app.py`
- `starter_kit/starter_kit/NOTAS.md` only if the implementation establishes a user-visible decision worth documenting
- This task document and its Engram mirror

## Delivery

- Strategy: `ask-on-risk`
- Forecast: fewer than 100 authored changed lines
- Chain strategy: not required
- Branch: `feat/typo-tolerant-retrieval`

## Testing Mode

- Mode: Standard; Strict TDD is disabled by existing project configuration.
- Runner: `/home/jero/Documentos/VentureLogic_Test/.venv/bin/python -m pytest`
- Require an observed failing focused regression before implementation, then focused and full GREEN.

## Tasks

- [x] **TTR-1 — Normalize the spelling variant and prove behavior**
  - Route: direct implementation; no delegation.
  - Added focused regression tests before the production change.
  - Normalized the targeted spelling family only for retrieval while preserving intent input and output question.
  - Commit: `7583758` (`fix(retrieval): normalize password reset spelling variant`).

## Acceptance Criteria

- `reestablezco`, `restablezco`, and uppercase equivalents classify as `cuenta`.
- Both spelling variants obtain equivalent retrieval evidence and produce `DUDOSO` for the supplied password-reset question.
- Returned `pregunta` remains byte-for-byte equal to user input.
- Protected retriever, fixtures, thresholds, and dependencies remain unchanged.
- Full pytest suite passes.

## Applicable Checks

- Focused: `.venv/bin/python -m pytest starter_kit/starter_kit/tests/test_app.py -v`
- Full: `.venv/bin/python -m pytest starter_kit/starter_kit`
- Integrity: `python -m tools.verify_delivery` from `starter_kit/starter_kit`
- Structural: `git diff --check`

## Progress and Evidence

- Status: TTR-1 complete.
- RED: focused suite `1 failed, 12 passed`; typo returned `SIN_EVIDENCIA` instead of canonical `DUDOSO`.
- GREEN: focused suite `13 passed in 0.04s`; full suite `61 passed in 0.17s`.
- Integrity: verifier passed all 7 protected hashes, canonical intents, and dependency checks; its expected pending correction remained reported. `git diff --check` passed.
- Runtime: canonical and typo inputs both returned `cuenta`, `DUDOSO`, score `0.566`, and their exact original questions.
- Authored line count: 99 additions plus deletions across the complete work-unit diff.
- Rollback boundary: revert this work unit's `app.py` normalization helper/use, regression test, and task evidence; no protected or unrelated behavior is involved.
