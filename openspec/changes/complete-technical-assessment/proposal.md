# Proposal: Complete Technical Assessment

## Intent

Complete all six exercises and every delivery obligation in `02_Prueba_Practica.pdf` so the supplied assistant becomes a deterministic, safe, locally runnable submission. The change must preserve protected inputs, add no dependencies, provide rubric-aligned tests and evidence, maintain an honest `NOTAS.md` throughout implementation, and remain reviewable through autonomous delivery slices under the 400-authored-line budget.

## Scope

### In Scope

- Implement the catalog-driven intent classifier in `config/intents.py`, including normalization, quoted-line exclusion, short-input rejection, longest-pattern selection, deterministic ties, and unknown fallback without changing `INTENTS`.
- Implement the asynchronous intent coverage report in `tools/intent_report_tool.py` using the supplied singleton clients, active-intent filtering, zero initialization, unknown-result preservation, useful logging, and propagated `KeyError` for a missing workspace.
- Repair `tools/legacy_answers_tool.py` while preserving its purpose: use singleton clients, eliminate unsafe process cache and shared `/tmp` output, avoid sequential N+1 source reads, return request-isolated data, and handle malformed or missing source data through an explicit logged per-answer policy.
- Add the strict verifier v2 prompt and fixture verdict matrix while preserving v1; require authoritative evidence metadata, literal citation validation, source validity, aligned `0.55`/`0.75` thresholds, strict JSON, and no response rewriting.
- Implement the session-and-agent-scoped, concurrency-safe `LoopGuard`, including limit behavior, actionable errors, isolated reset, and snapshot copies.
- Implement separately testable `consultar()` orchestration and a same-file, dependency-free safe web console that exposes intent, specialist, all fragments and scores, verdict, reason, and response or explicit abstention.
- Add or extend focused tests for exercises 2, 3, 5, and 6 while preserving supplied protected tests and testing exact threshold boundaries.
- Create and continuously maintain `NOTAS.md` with candidate identity, honest timing and completion status, confidence decisions, bounded conceptual notes, the legacy defect table, exact AI disclosure, one-week follow-up, and the required Enterprise abstention screenshot.
- Produce small incremental commits and autonomous review slices, splitting any slice that risks exceeding 400 authored changed lines.
- Verify the final result from a fresh clone: the declared pytest suite passes and `python app.py` serves `http://localhost:8000` locally without network access or credentials.

### Out of Scope

- Modifying `shared/clients.py`, `shared/retriever.py`, any file under `fixtures/`, `pytest.ini`, or `tests/test_classify_intent.py`.
- Adding packages, changing the declared dependency set, or growing `requirements.txt`.
- Replacing the protected lexical retriever, introducing semantic retrieval, or adding workspace filtering that its fixed API cannot support.
- Introducing a framework, external service, credential, network dependency, persistent cache, or production deployment architecture.
- Rewriting the assistant’s purpose or adding product features beyond the six exercises and mandatory submission evidence.
- Creating OpenSpec planning/change files as part of this Engram-backed SDD change.

## Capabilities

### New Capabilities

- `intent-classification`: Deterministically classify normalized Spanish messages from the protected intent catalog, including quoted-text exclusion, validation, longest-match precedence, deterministic ties, and unknown fallback.
- `intent-coverage-reporting`: Produce asynchronous per-workspace counts for active intents through singleton clients, retaining zero-count categories and safely mapping unsupported classifier output to `desconocido`.
- `legacy-answer-retrieval`: Return one workspace’s answers enriched with source titles without cross-request contamination, unsafe side effects, N+1 reads, or whole-request failure on malformed source records.
- `evidence-verification`: Define a strict, machine-readable verifier contract and expected fixture verdicts using literal citations, authoritative source metadata, source validity, traceability, and aligned similarity thresholds.
- `tool-loop-protection`: Enforce concurrency-safe tool-call limits independently per session and agent, with actionable failure details, isolated reset, and immutable snapshots.
- `assistant-console`: Run the classifier-to-retriever-to-specialist-to-verdict pipeline and render all evidence safely in a dependency-free local console with explicit approval, doubt, and abstention behavior.
- `assessment-delivery-compliance`: Provide protected-file enforcement, rubric-required tests and notes, honest evidence, incremental history, bounded review slices, and reproducible fresh-clone verification.

### Modified Capabilities

None. No existing SDD capability specifications were supplied; all assessment behavior is introduced as new capability contracts.

## Approach

Use dependency-first vertical delivery and update `NOTAS.md` in every slice rather than reconstructing evidence at the end:

1. Implement intent classification, run its protected contract, and record its bounded note.
2. Implement intent reporting with singleton and workspace-behavior tests.
3. Implement `consultar()` with deterministic pipeline and boundary tests.
4. Add safe console rendering and capture the three mandated demo outcomes, including Enterprise abstention evidence.
5. Repair legacy answer retrieval with focused contamination/error regression tests and complete the defect table.
6. Add verifier v2 and the fixture verdict matrix using authoritative evidence inputs and shared thresholds.
7. Implement the locked loop guard with complete isolation, reset, limit, and snapshot tests.
8. Finalize `NOTAS.md`, audit protected files/dependencies, and verify tests and serving from a fresh clone.

Each slice is an autonomous commit/review unit with its relevant tests and documentation, a clear rollback boundary, and an authored-line check. Under `auto-chain`, split a slice before review if it approaches 400 authored additions plus deletions; each child review targets the immediately preceding slice and must expose only its own diff.

Recommended decisions carried forward are: propagate missing-workspace `KeyError`; map classifications outside the active database set to `desconocido`; remove the legacy cache and shared temporary file; use `0.55` as minimum evidence and `0.75` as approval; reject invalid source references before considering DUDOSO; lock loop-guard state without holding the lock around external work; preserve catalog order for equal-length classifier ties; and treat `workspace_id` as request metadata because the protected retriever is global.

## Affected Areas

| Area | Impact | Description |
|---|---|---|
| `starter_kit/starter_kit/config/intents.py` | Modified | Exercise 1 classifier logic; `INTENTS` remains unchanged. |
| `starter_kit/starter_kit/tools/intent_report_tool.py` | Modified | Exercise 2 asynchronous singleton-backed coverage report. |
| `starter_kit/starter_kit/tools/legacy_answers_tool.py` | Modified | Exercise 3 isolation, batching, error handling, and side-effect removal. |
| `starter_kit/starter_kit/tools/loop_guard.py` | Modified | Exercise 5 concurrency-safe loop guard. |
| `starter_kit/starter_kit/app.py` | Modified | Exercise 6 orchestration and safe dependency-free console. |
| `starter_kit/starter_kit/prompts/verificador_v1.md` | Preserved | Read-only comparison baseline for exercise 4. |
| `starter_kit/starter_kit/prompts/verificador_v2.md` | New | Strict verifier prompt and JSON contract. |
| `starter_kit/starter_kit/prompts/casos_verificador.md` | New | Expected outcomes and reasons for fixture answers a-1 through a-5. |
| `starter_kit/starter_kit/tests/test_intent_report.py` | Modified | Mixed, empty, inactive, missing-workspace, and singleton-reuse coverage. |
| `starter_kit/starter_kit/tests/test_legacy_answers.py` | New | Regression coverage for severe cross-request contamination and selected malformed-record policy. |
| `starter_kit/starter_kit/tests/test_loop_guard.py` | Modified | Limit, isolation, reset, concurrency-policy, and snapshot coverage. |
| `starter_kit/starter_kit/tests/test_app.py` | Modified | DUDOSO, boundaries, empty/no-overlap, and pipeline output coverage. |
| `starter_kit/starter_kit/NOTAS.md` | New | Continuously maintained reasoning, timing, disclosure, defect analysis, and screenshot evidence. |
| Protected files and `requirements.txt` | Preserved | Verified unchanged throughout delivery and before submission. |

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| The declared pytest stack is not installed in the current host environment. | High | Use an isolated environment with only the already-declared development requirements, then repeat verification from a fresh clone without changing dependencies. |
| The repository has no baseline commit although incremental history is graded. | High | Establish a deliberate baseline before implementation and commit every autonomous vertical slice separately. |
| The full change exceeds the 400-authored-line review budget. | High | Use the eight auto-chained slices, measure additions plus deletions per slice, and split before review when necessary. |
| Verifier inputs omit authoritative source text or traceability metadata. | Medium | Make evidence fragments, source IDs, and chunk metadata mandatory parts of the verifier contract; reject invalid source references first. |
| Missing or corrupt legacy records cause data loss or abort a whole request. | Medium | Specify and regression-test a per-answer logged handling policy, batch source access, and return fresh request-owned structures. |
| Unsafe browser rendering exposes fixture or question text as HTML. | Medium | Render untrusted values with `textContent` or equivalent escaping and test/inspect the rendering path. |
| The protected retriever is not workspace-scoped. | Medium | Do not claim tenant filtering; preserve the protected API and document `workspace_id` as request metadata. |
| Required timing, identity, AI disclosure, and screenshot evidence become inaccurate if added late. | Medium | Update `NOTAS.md` during every slice and capture evidence from the actual final runtime. |
| The PDF’s cover references 72 hours while page 2 states no deadline. | Low | Record the ambiguity and obtain assessor clarification; do not let it alter implementation scope without explicit evidence. |

## Rollback Plan

Keep every vertical slice in its own commit and review branch. If a slice fails acceptance, revert that slice and any direct child slices while retaining the last passing chain point; rerun the tests owned by the reverted capability plus the full available suite. Never “roll back” by editing protected inputs or dependency declarations. For final-delivery failure, return to the latest fresh-clone-verified commit, regenerate only factual runtime evidence such as the screenshot or timestamps, and preserve the unsuccessful verification notes for auditability.

## Dependencies

- Python 3.10+ and the standard library for runtime behavior.
- Existing declared development requirements: `pytest>=8.0` and `pytest-asyncio>=0.23`; no additions are permitted.
- Supplied singleton clients, lexical retriever, deterministic fixtures, routing configuration, and protected tests.
- Git history for incremental commits and fresh-clone verification.
- A local browser or equivalent capture mechanism for the required Enterprise abstention screenshot.
- Candidate-provided identity and honest work timing for `NOTAS.md`.

## Success Criteria

- [ ] All six exercises satisfy their rubric requirements and every newly defined capability has passing acceptance scenarios.
- [ ] All 18 protected classifier cases pass without modifying `INTENTS` or `tests/test_classify_intent.py`.
- [ ] Intent reporting tests cover exact mixed counts, empty workspace, inactive-intent exclusion, propagated missing-workspace `KeyError`, unknown mapping, and singleton instantiation counts remaining one across repeated calls.
- [ ] Legacy retrieval has a regression test that fails against the original contamination defect and passes with fresh, isolated results; no process cache or shared `/tmp/last_answers.json` side effect remains.
- [ ] Verifier v2 emits strict JSON, does not rewrite answers, validates literal/source traceability, uses `0.55`/`0.75`, and documents a-1 APROBADO, a-2 RECHAZADO, a-3 APROBADO, a-4 RECHAZADO, and a-5 DUDOSO with reasons.
- [ ] LoopGuard permits calls through `MAX_CALLS`, raises on `MAX_CALLS + 1`, isolates session/agent keys, resets only one session, returns snapshot copies, and protects shared state with a standard-library lock.
- [ ] `consultar()` preserves every retrieved fragment, selects the top score, and returns exact SIN_EVIDENCIA below `0.55` or with no fragments, DUDOSO from `0.55` to below `0.75`, and APROBADO at or above `0.75`, with reasons citing observed values and thresholds.
- [ ] The console safely shows the three mandated demo questions as APROBADO, DUDOSO, and SIN_EVIDENCIA and visibly abstains for the Enterprise-plan question without rendering untrusted text as HTML.
- [ ] Protected files are byte-for-byte unchanged and `requirements.txt` contains no new dependency.
- [ ] `NOTAS.md` contains every required identity, timing, completion, decision, conceptual-note, defect-table, AI-disclosure, screenshot, and one-week-follow-up item with honest values.
- [ ] Git history contains multiple small, coherent commits aligned to autonomous delivery slices; no review slice exceeds 400 authored changed lines without being split.
- [ ] From a fresh clone, the declared pytest suite passes and `python app.py` serves `http://localhost:8000` without network access or credentials.

## Unresolved Decisions

- The candidate name, actual start/delivery timestamps, real hours per exercise, exact AI-use disclosure, and screenshot must be supplied from real implementation activity; they cannot be truthfully predetermined in planning.
- The PDF’s 72-hour cover reference conflicts with the page-2 statement that there is no deadline and requires assessor clarification.
- The exact per-answer result shape for a missing/corrupt legacy source should be finalized in specs/design; the governing decision is to log and isolate the affected answer rather than abort or contaminate the full request.
