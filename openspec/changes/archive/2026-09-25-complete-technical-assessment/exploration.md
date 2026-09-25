## Exploration: Complete Technical Assessment

### Current State
The repository is an intentionally incomplete, local-only Python 3.10+ assistant skeleton. Its runtime pipeline is classifier → lexical retriever → specialist routing → evidence verdict → final response. `shared/clients.py` supplies fixture-backed asynchronous singleton clients, `shared/retriever.py` supplies deterministic lexical retrieval, and `app.py` contains a standard-library HTTP server with an unimplemented `consultar()` and a raw-JSON page. Exercises 1, 2, 5, and 6 currently raise `NotImplementedError`; exercise 3 deliberately contains production defects; exercise 4 has only the permissive v1 verifier prompt.

The assessment contains six exercises totaling 100 points. The actual baseline suite cannot currently run because `pytest` is declared but not installed (`python3 -m pytest` reports `No module named pytest`). The Git repository has no commits yet. Directly exercising the protected retriever confirms the supplied thresholds: the Pro warranty query scores `1.0` (APROBADO), password reset scores `0.566` (DUDOSO), and Enterprise warranty scores `0.373` (SIN_EVIDENCIA); an empty query returns no fragments.

#### Assessment requirement map

| Exercise | Required implementation and protected inputs | Required tests / evidence | Acceptance criteria and documentation |
| --- | --- | --- | --- |
| 1 — Intent classifier (15) | Implement `classify_intent()` in `config/intents.py`; do not alter `INTENTS`. Normalize once for case, accents/ñ, punctuation, and spacing; discard lines beginning with `>`; reject empty/short normalized input; select the longest matching configured pattern; otherwise return `desconocido`. | `tests/test_classify_intent.py` is protected and must remain unchanged; all 18 parameterized cases must pass. | Generic catalog-driven logic, no message-specific hacks. Add the rules-vs-LLM note to `NOTAS.md` (≤120 words), including one concrete advantage, one disadvantage, and a switch condition. |
| 2 — Intent coverage report (15) | Implement async `count_messages_by_intent()` in `tools/intent_report_tool.py`. Read active intents through `get_db_client()`, messages through `get_storage_client()`, await both APIs, classify through exercise 1, initialize zero counts, always include `desconocido`, exclude inactive intents, and log useful context. Do not instantiate clients. | Extend `tests/test_intent_report.py` by at least four tests: exact mixed counts, empty workspace, inactive `ventas` absent, chosen missing-workspace behavior, and singleton reuse. The singleton assertion should prove repeated calls keep each `_INSTANTIATIONS` count at one. | Decide and comment on missing workspace behavior. Recommended: propagate `KeyError`, preserving the distinction between a nonexistent workspace and a valid empty workspace. Any classifier result outside the active DB set should be counted as `desconocido` so totals are not silently lost. |
| 3 — Legacy code review (20) | Correct `tools/legacy_answers_tool.py` without changing its purpose: return one workspace’s answers enriched with source titles. The real defects include a mutable process cache; a cache key that ignores `min_similitud`; shared mutable cached results; direct `DatabaseClient()` construction; sequential N+1 source reads; unchecked missing source/data fields that can abort the request; a shared, non-atomic `/tmp/last_answers.json` side effect that leaks/overwrites tenant data and does not survive stateless deployment; unbounded/stale process-local state; and underspecified threshold/error behavior. | Add a focused regression test (recommended `tests/test_legacy_answers.py`) that fails against the original severe cross-request contamination behavior and passes after repair. | `NOTAS.md` needs one row per defect with line, problem, concrete production symptom, and severity; at least six are scored, and extra valid findings count. Prefer removing unreliable cache/file side effects, using the singleton, returning fresh data, and handling missing source records per answer with an explicit logged policy rather than crashing the whole process. |
| 4 — Verifier prompt (15) | Keep `prompts/verificador_v1.md`; create concise `prompts/verificador_v2.md` and `prompts/casos_verificador.md`. V2 must define literal-citation checks, reject generic paraphrases, add DUDOSO for real evidence with missing traceability metadata, use and justify similarity, forbid rewriting, and require strict JSON with an input/output example. | Document expected verdicts for fixture answers a-1 through a-5 and one-line reasons. Recommended outcomes: a-1 APROBADO; a-2 RECHAZADO (generic/nonliteral citation and 0.34); a-3 APROBADO; a-4 RECHAZADO (the trap: nonexistent/mismatched `source_id` despite plausible text); a-5 DUDOSO (real citation and 0.86 but missing chunk). | The verifier input must include the authoritative retrieved fragment/source metadata; otherwise literalness and source validity cannot be checked. Align thresholds with the console (`0.55` minimum, `0.75` approval): below minimum rejects; acceptable evidence lacking traceability is DUDOSO; complete evidence at/above high threshold can approve. Explain why review is preferable to rejection for usable evidence with incomplete metadata. Add the deterministic-verification note to `NOTAS.md` (≤120 words). |
| 5 — Anti-loop guard (10) | Implement `LoopGuard` and `ToolLoopError` behavior in `tools/loop_guard.py`: counts keyed by `(session_id, agent_name)`, allow through `MAX_CALLS`, raise on `MAX_CALLS + 1`, actionable error including agent/session/count, isolate agents and sessions, reset one session, and return snapshot copies. | Fully write `tests/test_loop_guard.py` for every listed behavior, including reset isolation and snapshot state. | Add a concurrency comment. Recommended implementation protects shared state with a standard-library lock because the stated production model includes parallel specialists; never hold the lock across external work. Add the central interception-point note to `NOTAS.md` (≤150 words), placing the guard in the shared tool-dispatch/execution boundary rather than duplicating it inside tools. |
| 6 — Assistant console (25) | Implement async `consultar()` in `app.py` as separately testable core logic: classify, resolve specialist, await protected `shared.retriever.search`, preserve all fragments, select the top score, and emit the exact documented dictionary. At `<0.55` or no fragments return SIN_EVIDENCIA and `respuesta: None`; at `0.55 ≤ score < 0.75` return DUDOSO with the top fragment text; at `≥0.75` return APROBADO with the top fragment text. Every `motivo` must cite observed values and thresholds. Replace raw JSON rendering with one same-file, dependency-free page showing intent, specialist, fragments/scores, verdict, reason, and response/clear abstention. | Keep the two supplied tests and add at least DUDOSO plus one boundary/empty/no-overlap test. Test exact threshold boundaries through a patched retriever. The three mandated demo questions must visibly produce APROBADO, DUDOSO, and SIN_EVIDENCIA. | Use only the standard library and do not change the protected retriever. Render untrusted question/fixture text via `textContent` or equivalent escaping, not interpolated `innerHTML`. If thresholds change, justify them in `NOTAS.md`; retaining them is recommended because measured fixture scores intentionally straddle them. Add the semantic-retrieval improvement note to `NOTAS.md` (≤120 words). |

#### Cross-cutting delivery obligations

- Create mandatory `NOTAS.md` with: candidate name; completed/incomplete summary; honest start/delivery times and real hours by exercise; three high-confidence decisions; two low-confidence decisions and reversal evidence; all four bounded conceptual notes; exercise 3 defect table; exact AI tool/use disclosure; and what would be done with one more week.
- Include in `NOTAS.md` a screenshot of the running console answering the Enterprise-plan question and visibly abstaining.
- Use real, small commits while progressing, not one final commit. The repository currently has no commits, so implementation should establish a clean baseline/history deliberately without committing the supplied assessment PDF unless desired by the owner.
- Before delivery, verify from a fresh clone that `pytest` passes and `python app.py` serves `http://localhost:8000` without network or credentials.
- Keep `shared/clients.py`, `shared/retriever.py`, all `fixtures/`, `pytest.ini`, and `tests/test_classify_intent.py` unchanged. Do not add dependencies or grow `requirements.txt`.
- The expected submission tree adds `NOTAS.md`, `prompts/verificador_v2.md`, `prompts/casos_verificador.md`, and an exercise 3 regression test while modifying only the allowed exercise files/tests.
- The full change will likely exceed the 400 authored-line review budget. With the preflight `auto-chain` strategy, plan autonomous slices with their own tests and documentation rather than one oversized review.

### Affected Areas
- `starter_kit/starter_kit/config/intents.py` — exercise 1 classifier implementation; catalog remains unchanged.
- `starter_kit/starter_kit/tools/intent_report_tool.py` — exercise 2 async singleton-backed report.
- `starter_kit/starter_kit/tools/legacy_answers_tool.py` — exercise 3 defect correction while preserving behavior.
- `starter_kit/starter_kit/tools/loop_guard.py` — exercise 5 stateful guard and concurrency policy.
- `starter_kit/starter_kit/app.py` — exercise 6 pipeline and single-page console.
- `starter_kit/starter_kit/prompts/verificador_v1.md` — read-only baseline for exercise 4.
- `starter_kit/starter_kit/prompts/verificador_v2.md` — new strict verifier prompt.
- `starter_kit/starter_kit/prompts/casos_verificador.md` — new fixture verdict matrix.
- `starter_kit/starter_kit/tests/test_intent_report.py` — at least four additional exercise 2 tests.
- `starter_kit/starter_kit/tests/test_loop_guard.py` — complete exercise 5 suite.
- `starter_kit/starter_kit/tests/test_app.py` — at least two additional exercise 6 tests.
- `starter_kit/starter_kit/tests/test_legacy_answers.py` — recommended new exercise 3 regression test.
- `starter_kit/starter_kit/NOTAS.md` — mandatory reasoning, timing, defects, AI disclosure, screenshot, and completion status.
- `starter_kit/starter_kit/shared/clients.py`, `shared/retriever.py`, `fixtures/`, `pytest.ini`, `tests/test_classify_intent.py`, `requirements.txt` — protected or dependency-frozen inputs that constrain all implementation.

### Approaches
1. **Dependency-first vertical delivery** — Implement and verify 1 → 2 → 6 first, then 3 → 4 → 5, updating `NOTAS.md` and tests in each slice.
   - Pros: Follows the PDF’s explicit priority path; produces the highest-value runnable console early; validates thresholds and integration before peripheral work; supports small autonomous chained reviews.
   - Cons: Exercise numbering is not followed strictly; later work can still affect shared review/documentation decisions.
   - Effort: High

2. **Strict numeric exercise order** — Complete 1 through 6 sequentially and assemble documentation near the end.
   - Pros: Simple progress tracking; mirrors the rubric exactly.
   - Cons: Delays the 25-point runnable console; encourages a large late integration/debugging phase; increases risk of forgetting evidence and timing notes.
   - Effort: High

### Recommendation
Use dependency-first vertical delivery, but update `NOTAS.md` continuously rather than reconstructing reasoning at the end. Suggested review/commit slices are: (1) classifier plus fixed-contract verification and note; (2) intent report plus tests; (3) `consultar()` plus pipeline tests; (4) safe console rendering plus demo evidence; (5) legacy repair plus regression and defect table; (6) verifier prompt/cases; (7) loop guard/tests; (8) final notes and fresh-clone verification. Keep each slice independently understandable and tested; split further when the 400-line authored budget is at risk.

Resolve genuine decisions consistently: propagate missing-workspace `KeyError` in exercise 2; treat out-of-active-set classifications as unknown; remove process-local legacy cache and shared `/tmp` output rather than trying to make them authoritative; use 0.55/0.75 across verifier and console; reject invalid source references before considering DUDOSO; use a lock in `LoopGuard`; retain the protected lexical retriever and treat `workspace_id` as request metadata because the supplied retriever has no workspace parameter.

### Risks
- `pytest` is not installed, so no baseline or future suite result is currently available until the declared development dependencies are installed in a virtual environment.
- The repository has no commits yet, while the assessment explicitly grades incremental history; commit planning must begin with the first implementation slice.
- The verifier cannot establish literal citation or source validity unless its input contract includes authoritative evidence text and metadata.
- `shared.retriever.search()` is global rather than workspace-scoped; modifying it is forbidden, so tenant isolation cannot be added in exercise 6 without violating the assessment.
- Exercise 3 permits several repair policies for missing/corrupt records; whichever policy is selected must be reflected in the regression tests and defect table.
- Classifier ties between equally long patterns are unspecified; preserve deterministic catalog order and document only if a tie is encountered.
- The PDF cover mentions 72 hours while page 2 states no deadline; this is a process ambiguity, not an implementation blocker, and should be clarified with the assessor or recorded in delivery notes.
- The total work is likely above 400 authored changed lines; auto-chained review slices are needed to avoid an oversized final review.

### Ready for Proposal
Yes. The six exercises, protected boundaries, implementation targets, tests, documentation, delivery obligations, and acceptance criteria are sufficiently explicit. The proposal should preserve the recommended decisions above, make `NOTAS.md` a continuous deliverable, and plan the work as dependency-first chained slices under the 400-line review budget.
