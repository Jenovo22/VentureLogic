# Feature: Final Delivery Compliance

## Objective

Make the published assessment conform exactly to the delivery and documentation requirements in `02_Prueba_Practica.pdf` without changing protected behavior or historical audit artifacts.

## Problem and Why

The implementation passes all current checks, but the final audit found explicit PDF gaps: no start time, fewer than six defect-table rows, missing business justification for `DUDOSO`, stale starter-era instructions/evidence, and a nested `starter_kit/starter_kit` layout instead of the required `entrega_<tu_nombre>/` package.

## Scope

- Correct final delivery documentation using observed facts only.
- Preserve every protected file and dependency declaration byte-for-byte.
- Move the tracked runnable package mechanically to `entrega_jeronimo_novoa_giraldo/`.
- Keep supplied PDF, OpenSpec archive/canonical specs, ODD history, and Git history intact.
- Verify tests, integrity, HTTP demos, screenshot, and a clean local clone from the final committed candidate.
- Do not push, create a PR, or merge without a separate explicit remote authorization.

## Candidate Facts

- Candidate: Jeronimo Novoa Giraldo.
- Start: 24/09/2026 at 14:00.
- Final delivery timestamp must be recorded from the actual final verification time.

## Delivery

- Strategy: `ask-on-risk`.
- Forecast: below 400 authored lines excluding mechanical renames and existing binary bytes.
- Branch: `fix/final-delivery-compliance`.
- TDD: disabled by project configuration; use behavior-first regression checks and full verification.

## Tasks

- [x] **FDC-1 — Correct PDF-mandated documentation**
  - Route: direct implementation; no delegation.
  - Trigger evidence: preparation requires PDF, historical baseline, prompts, notes, README, and app context across more than four files.
  - Add at least six distinct legacy defects, explicit business rationale for `DUDOSO`, start time, current test evidence, consistent scores/hours, and final-state startup guidance.
  - Remove or clearly mark obsolete starter-era statements without rewriting historical RED evidence.
  - Close with a Conventional Commit and exact verification evidence.

- [ ] **FDC-2 — Build the required delivery package**
  - Route: direct implementation; no delegation.
  - Mechanically move the tracked runnable package from `starter_kit/starter_kit/` to `entrega_jeronimo_novoa_giraldo/`.
  - Preserve file bytes during the move except explicitly authorized documentation/application-comment corrections.
  - Add repository ignore rules for local environments, CodeGraph, Python caches, test caches, and OS metadata.
  - Confirm every PDF-listed path exists under the delivery package and close with a Conventional Commit.

- [ ] **FDC-3 — Prove final delivery from committed bytes**
  - Route: direct implementation; no delegation.
  - Run focused/full tests, delivery verifier, three HTTP demonstrations, screenshot validation, protected hashes, dependency audit, and `git diff --check` from the new layout.
  - Clone the committed candidate into a clean directory under the authorized workspace, run pytest/verifier/server without network or credentials, then remove temporary state.
  - Record the actual final delivery timestamp and evidence, close with a Conventional Commit receipt, and leave no tracked changes.

## Acceptance Criteria

- All explicit PDF requirements classify PASS with no documentation blocker.
- `entrega_jeronimo_novoa_giraldo/NOTAS.md`, `app.py`, required config/tools/prompts/tests, screenshot, fixtures, shared modules, `requirements.txt`, and `pytest.ini` are present.
- Start time is `24/09/2026 14:00`; delivery time is factual and current.
- Legacy defect table has at least six distinct rows with line/location, problem, production symptom, and severity.
- Verifier explains why valid evidence with incomplete traceability should enter review rather than be discarded.
- Current evidence says 61 tests and uses the observed password score `0.566`.
- Protected hashes, canonical `INTENTS`, dependencies, screenshot, and all runtime behavior remain valid.
- Clean-clone pytest, verifier, and `python app.py` succeed from the final package.

## Progress and Evidence

- Status: FDC-1 complete; FDC-2 pending; FDC-3 pending.
- FDC-1 evidence:
  - Inspected the original `tools/legacy_answers_tool.py` bytes from baseline commit `dfbcea2` and documented eight distinct, concrete defects without altering the corrected implementation.
  - Corrected the start time to `24/09/2026 14:00`; final delivery time remains explicitly pending until FDC-3 observes it.
  - Recorded current post-typo evidence: 61/61 tests and password score `0.566`; retained earlier RED and pre-typo `0.666` evidence as explicitly historical chronology.
  - Added the business rationale for review-only `DUDOSO`, final local startup/test instructions, and removed stale implementation-missing comments without runtime changes.
  - Conceptual word-count check: Exercise 1 = 107/120, Exercise 4 = 114/120, Exercise 5 = 117/150, Exercise 6 = 97/120.
  - Focused verification: `/home/jero/Documentos/VentureLogic_Test/.venv/bin/python -m pytest` from the package root passed 61/61 in 0.16 s.
  - Runtime boundary: N/A for this documentation-only correction; HTTP behavior is unchanged and will be proved in FDC-3.
  - Rollback boundary: revert only `NOTAS.md`, `README.md`, `prompts/verificador_v2.md`, the stale comments/docstring in `app.py`, and this FDC-1 evidence block.
- Next step: complete the mechanical FDC-2 package move.
