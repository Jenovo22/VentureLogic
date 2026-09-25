# Design: Complete Technical Assessment

## Executive Design

Implement the seven specified capabilities inside the existing Python/standard-library boundaries, in dependency order: classifier → coverage report → query pipeline → safe browser console, followed by isolated legacy repair, verifier v2, loop protection, and final delivery evidence. Preserve every protected input and the current public result schemas, reuse the supplied singleton clients, and keep all behavior deterministic and local.

The repository is an unborn Git worktree, so a provenance-preserving baseline commit and protected-file hash manifest must exist before implementation edits. Delivery then uses a Feature Branch Chain because intermediate assessment states intentionally retain unrelated placeholder failures and should not land independently. Each child review contains one vertical work unit, its tests, and its contemporaneous `NOTAS.md` update, with an authored additions-plus-deletions budget of 400 lines.

CodeGraph was unavailable in `PATH`, and its required initialization had already failed. This design therefore used bounded reads of the actual application, shared clients/retriever, fixtures, prompts, tests, dependency declarations, and control-plane configuration.

## Technical Approach

### Capability map

| Capability | Implementation approach | Primary verification |
|---|---|---|
| Intent classification | Normalize eligible non-quoted lines once; match normalized catalog patterns on token boundaries; select the longest pattern and preserve catalog order for equal lengths. | Unchanged 18-case protected suite plus catalog/tie-focused checks only if needed outside the protected file. |
| Intent coverage reporting | Acquire `get_db_client()` and `get_storage_client()`, await both APIs, initialize active intents plus `desconocido`, and preserve every message in totals. | Mixed, empty, inactive, unknown, missing-workspace, error logging, and repeated singleton-use tests. |
| Legacy answer retrieval | Filter by inclusive threshold, fetch all sources once, enrich valid answers into fresh dictionaries, and omit invalid-source answers while recording pending corrections. | Isolation, mutation, threshold, singleton, one-batch source fetch, and each omission-reason test. |
| Evidence verification | Add a strict prompt-only v2 contract and deterministic a-1…a-5 fixture matrix while retaining v1. | JSON examples parsed during review; matrix checked against protected fixture facts and exact 0.55/0.75 boundaries. |
| Tool-loop protection | Protect per-session/per-agent counters with `threading.Lock`; reject the first excess call without advancing stored state beyond the limit. | Limit, actionable error, isolation, reset, snapshot-copy, and concurrent update tests. |
| Assistant console | Keep `consultar()` as the async core and `Handler` as an HTTP adapter; preserve all fragments, compute the top fragment, apply exact boundaries, and render only through DOM `textContent`. | Unit boundary tests, HTTP/browser smoke, inert-markup inspection, and the required Enterprise abstention screenshot. |
| Delivery compliance | Capture a pre-edit integrity baseline, maintain `NOTAS.md` continuously, expose pending corrections through a standard-library verifier, and verify a fresh local clone. | Full pytest, protected/dependency audit, ledger report, local HTTP smoke, clean-diff/line-budget receipts. |

### Delivery sequence

```text
Supplied baseline + protected hashes
              │
              ▼
Classifier ──→ Intent report ──→ consultar() ──→ Safe console
                                                   │
                                                   ▼
Legacy repair + ledger ──→ Verifier v2 ──→ LoopGuard
                                                   │
                                                   ▼
                         final notes + integrity + fresh-clone evidence
```

`NOTAS.md` is created with explicit incomplete placeholders in the first slice and updated in every later slice. Identity, timestamps, hours, AI disclosure, completion state, and screenshot evidence are written only from real activity.

## Architecture Decisions

### Decision: Preserve the existing module boundaries and dependency set

**Choice**: Implement behavior in `config/`, `tools/`, and `app.py`, adding only focused standard-library audit support and evidence files.

**Alternatives considered**: Add a web framework, validation package, persistent database, or restructure the starter into new application layers.

**Rationale**: The assessment explicitly freezes dependencies and supplies clear module ownership. A framework or broad rewrite would increase review surface, obscure the intended exercises, and violate the no-new-dependency contract.

### Decision: Normalize and match classifier text deterministically

**Choice**: Drop lines whose first non-space character is `>`, join remaining lines, apply Unicode decomposition, remove combining marks (including the tilde from `ñ`), lowercase, replace non-alphanumeric runs with one space, and trim. Reject normalized strings shorter than `MIN_LENGTH`. Evaluate catalog patterns in existing dictionary/list order, require token-boundary phrase matches, and replace the winner only when a strictly longer pattern is found.

**Alternatives considered**: Raw substring matching, per-pattern normalization, regex exceptions for supplied messages, or an LLM classifier.

**Rationale**: One normalization pass is generic and deterministic. Token boundaries avoid accidental interior-word matches. Strictly-greater replacement naturally preserves catalog order for equal lengths without mutating `INTENTS`.

### Decision: Reuse shared singleton clients and propagate operational errors

**Choice**: `count_messages_by_intent()` and legacy retrieval call `get_db_client()`/`get_storage_client()`; they never construct clients. A missing report workspace logs the workspace identifier and propagates `KeyError`; all other client failures are logged with operation/workspace context and propagated without message bodies or credentials.

**Alternatives considered**: Return zeros for a missing workspace, swallow errors, or instantiate isolated clients per call.

**Rationale**: Propagation preserves the semantic difference between missing and empty workspaces, while singleton reuse is an explicit production and test invariant.

### Decision: Batch legacy source resolution and preserve request ownership

**Choice**: Fetch workspace answers once, apply `similitud >= min_similitud`, and return immediately when none qualify. Otherwise fetch the `sources` table once, index records by `Record.id`, and build new answer dictionaries. Never cache request results and never write `/tmp/last_answers.json`.

**Alternatives considered**: Keep a corrected process cache, include the threshold in a cache key, issue concurrent per-source item reads, or continue sequential N+1 reads.

**Rationale**: The supplied API supports a single table read but no `IN` query. One batched read is simpler and safer than many awaits, and fresh dictionaries prevent cross-workspace, cross-threshold, and caller-mutation contamination.

### Decision: Persist invalid-source omissions in an append-only pending ledger

**Choice**: Add `tools/correction_ledger.py` with a process-thread-safe `PendingCorrectionLedger`. Its default store is `evidence/pending_source_corrections.jsonl`; tests inject a `tmp_path` ledger. Each unique pending defect records schema version, `status: "pending"`, workspace ID, answer ID, source ID (including missing/null), a reason code (`missing_source`, `malformed_source`, or `missing_title`), diagnostic detail, and first-observed UTC time. Recording and logging occur before the answer is omitted. Existing valid answers and their schema remain unchanged.

The JSONL writer holds a `threading.Lock`, checks existing stable keys to avoid duplicate pending defects, and appends one complete UTF-8 JSON line with flush/fsync. It never writes to `/tmp`, never edits protected data, and never attempts remediation. `tools/verify_delivery.py` parses the ledger, prints every unresolved record or an explicit zero count, and treats malformed ledger syntax as verification failure. Pending records are reported honestly but do not make valid partial retrieval fail.

**Alternatives considered**: Expand returned answers with an unavailable marker, keep an in-memory list, rely only on logs, write into `NOTAS.md` at request time, or repair fixtures automatically.

**Rationale**: A dedicated durable ledger is auditable across process restarts without changing the current result schema. Logs alone are not a ledger; process memory is not durable; mutating documentation at runtime is unsafe. Remediation remains a separate final-phase decision requiring explicit user authorization.

### Decision: Align all evidence decisions to exact shared boundaries

**Choice**: Retain `UMBRAL_MINIMO = 0.55` and `UMBRAL_ALTO = 0.75`. `consultar()` uses `score < 0.55` → `SIN_EVIDENCIA`, `0.55 <= score < 0.75` → `DUDOSO`, and `score >= 0.75` → `APROBADO`. Verifier v2 uses below 0.55 → `RECHAZADO`; valid evidence from 0.55 to below 0.75 cannot be approved; complete evidence at or above 0.75 may be approved. Invalid source identity always produces `RECHAZADO` before missing traceability can produce `DUDOSO`.

**Alternatives considered**: Round scores before comparison, use different verifier and console thresholds, or make equality implementation-dependent.

**Rationale**: Direct numeric comparison preserves the specified inclusive/exclusive boundaries. Shared constants in prose and tests prevent semantic drift while respecting that console abstention and verifier rejection use different verdict vocabularies.

### Decision: Keep `consultar()` independent from HTTP and preserve the exact response shape

**Choice**: `consultar()` classifies, resolves `specialist_for()`, awaits protected `search()`, copies every returned fragment into the `fragmentos` list, selects the maximum raw `similitud`, and derives verdict/reason/response. `workspace_id` remains request metadata because protected `search()` is global and accepts no workspace parameter. The response contains exactly `pregunta`, `workspace`, `intencion`, `especialista`, `fragmentos`, `veredicto`, `motivo`, and `respuesta`; the top fragment is identified in the UI by object position/identity rather than a schema extension.

**Alternatives considered**: Put orchestration in `Handler`, modify the protected retriever to add workspace filtering, discard lower-ranked fragments, or add an undocumented top-evidence field.

**Rationale**: This keeps core behavior directly testable, does not claim tenant filtering the supplied API cannot perform, and preserves the exact contract consumed by current tests and page code.

### Decision: Render browser data with DOM text sinks only

**Choice**: The same-file page builds result sections with `document.createElement`, assigns all question, fragment, source, reason, and response values through `textContent`, and never interpolates response values into HTML or uses `innerHTML`. It visibly labels APROBADO, DUDOSO, and SIN_EVIDENCIA, marks the selected fragment, and shows an explicit abstention when `respuesta` is null. Both query and workspace parameters are URL-encoded.

**Alternatives considered**: Continue raw JSON, build HTML strings with escaping, or add a client framework.

**Rationale**: DOM text sinks make fixture/question markup inert by construction and avoid maintaining a custom escaping routine without adding dependencies.

### Decision: Make LoopGuard mutation atomic and snapshots caller-owned

**Choice**: Store counts by `(session_id, agent_name)` and guard record/reset/snapshot operations with one `threading.Lock`. Calls 1 through `max_calls` update and return the count. Attempt `max_calls + 1` raises `ToolLoopError` containing session, agent, attempted count, and limit while stored state remains capped. `reset()` removes only keys for the requested session; `snapshot()` constructs a new dictionary while locked and returns it after releasing the lock.

**Alternatives considered**: No lock under the GIL, an async lock, or holding the lock around tool execution.

**Rationale**: Read-modify-write sequences are not a safe concurrency contract merely because CPython has a GIL. The guard is synchronous shared state, so a standard lock is appropriate; external work never occurs under it.

### Decision: Treat verifier v2 as a strict, non-rewriting evidence protocol

**Choice**: `verificador_v2.md` requires input fields for answer ID, candidate answer, claimed citation/source/chunk, similarity, and authoritative retrieved source/chunk/title/text. Output is JSON only:

```json
{
  "answer_id": "a-1",
  "veredicto": "APROBADO",
  "motivo": "Literal citation, valid source/chunk traceability, and similarity 0.91 >= 0.75.",
  "checks": {
    "cita_literal": true,
    "fuente_valida": true,
    "trazabilidad_completa": true,
    "similitud_suficiente": true
  }
}
```

No revised-answer field is permitted. `casos_verificador.md` records a-1 APROBADO, a-2 RECHAZADO, a-3 RECHAZADO, a-4 RECHAZADO, and a-5 DUDOSO with one-line evidence-grounded reasons. For a-3, the nonliteral `Configuración > Equipo` citation deterministically fails before its valid `src-2` source and `0.88` similarity can approve it.

**Alternatives considered**: Return approved answers, allow prose around JSON, let the verifier improve answers, or infer source validity from a source ID alone.

**Rationale**: Literalness and source ownership cannot be established without authoritative evidence. A closed JSON contract is machine-readable and prevents the verifier from silently becoming a generator.

### Decision: Enforce protected-file integrity from a pre-edit manifest

**Choice**: Before implementation, create `evidence/protected_baseline.json` containing SHA-256 values for `shared/clients.py`, `shared/retriever.py`, every fixture file, `pytest.ini`, `tests/test_classify_intent.py`, and `requirements.txt`, plus a canonical JSON hash of the `INTENTS` AST literal. `tools/verify_delivery.py` checks those values and confirms the dependency declaration has not expanded. The baseline must never be regenerated after implementation merely to make verification pass.

**Alternatives considered**: Rely on Git diff despite the unborn repository, hash all of `config/intents.py`, or trust manual review.

**Rationale**: The classifier function must change while `INTENTS` must not, so whole-file hashing is insufficient there. The repository has no initial commit, making an independent pre-edit manifest necessary.

### Decision: Use a Feature Branch Chain with vertical review units

**Choice**: First preserve the supplied starter kit as an explicit baseline commit; then use a draft/no-merge `feat/complete-technical-assessment` tracker. Child review 1 targets the tracker branch and each later child targets the immediate prior child. Measure authored additions plus deletions per child; split any child over 400 lines once by cohesive behavior, never by deleting tests/docs or compressing code.

**Alternatives considered**: One PR, file-type commits, or stacked PRs landing partial exercises directly on the main branch.

**Rationale**: The total change is high risk for the 400-line budget, while intermediate branches intentionally retain unrelated exercise failures. A feature chain protects main, preserves dependency order, and presents only one reviewed vertical delta at a time.

## Data Flow

### Intent coverage

```text
workspace_id
    │
    ├──→ get_db_client() ──await intents.get()──→ active intent IDs
    │
    └──→ get_storage_client() ──await list_messages()──→ messages
                                                        │
                                      classify_intent() ─┘
                                                        │
                    active result ──→ exact bucket      │
                    inactive/unknown ──→ desconocido ───┘
```

### Query pipeline and console

```text
GET /api/consulta?q=...&ws=...
          │
          ▼
       Handler ──→ consultar(question, workspace metadata)
                         │
                classify_intent() ──→ specialist_for()
                         │
                         └──await search(question)──→ all fragments
                                                       │
                                         max similarity + 0.55/0.75
                                                       │
          JSON response ◀── exact result dictionary ◀──┘
                 │
                 ▼
       DOM nodes + textContent only
```

### Legacy retrieval and omission audit

```text
workspace_id + min_similitud
          │
          ▼
answers.where(...).get() ──→ inclusive threshold filter
          │                           │
          │                           └── none ──→ fresh []
          ▼
sources.get() once ──→ {source_id: source data}
          │
          ├── valid source/title ──→ fresh enriched answer
          │
          └── invalid source/title ──→ structured log
                                      + PendingCorrectionLedger.record()
                                      + omit from current result
```

### Verification flow

```text
pre-edit protected inputs ──SHA-256/canonical INTENTS──→ protected_baseline.json
final tree ──tools/verify_delivery.py──→ integrity/dependency result
                                      └→ pending ledger: 0 or full unresolved list
fresh local clone ──pytest + app startup/browser smoke──→ factual NOTAS.md evidence
```

## File Changes

| File | Action | Description |
|---|---|---|
| `starter_kit/starter_kit/config/intents.py` | Modify | Implement one-pass normalization, quoted-line exclusion, minimum length, boundary-aware longest match, catalog-order tie behavior, and unknown fallback without changing `INTENTS`. |
| `starter_kit/starter_kit/tools/intent_report_tool.py` | Modify | Add asynchronous active-intent counting with singleton clients, unknown preservation, error propagation, and non-sensitive logs. |
| `starter_kit/starter_kit/tools/legacy_answers_tool.py` | Modify | Remove mutable cache/direct client/shared temp output, batch sources, return fresh data, and invoke the omission ledger. |
| `starter_kit/starter_kit/tools/correction_ledger.py` | Create | Standard-library, thread-safe JSONL pending-correction ledger with injectable path and stable reason codes. |
| `starter_kit/starter_kit/tools/verify_delivery.py` | Create | Verify protected hashes/dependencies and print every unresolved ledger record or explicit zero count. |
| `starter_kit/starter_kit/tools/loop_guard.py` | Modify | Implement locked per-session/per-agent accounting, actionable limit errors, isolated reset, and copied snapshots. |
| `starter_kit/starter_kit/app.py` | Modify | Implement async orchestration and replace raw JSON output with complete, safe DOM rendering. |
| `starter_kit/starter_kit/prompts/verificador_v2.md` | Create | Define authoritative evidence input, strict JSON output, source/literal/traceability checks, exact thresholds, and no rewriting. |
| `starter_kit/starter_kit/prompts/casos_verificador.md` | Create | Document deterministic a-1 through a-5 verdicts and reasons. |
| `starter_kit/starter_kit/tests/test_intent_report.py` | Modify | Add mixed/empty/inactive/missing/error/unknown/singleton coverage. |
| `starter_kit/starter_kit/tests/test_legacy_answers.py` | Create | Add isolation, batching, threshold, omission, ledger, and valid-partial-result regression coverage. |
| `starter_kit/starter_kit/tests/test_loop_guard.py` | Modify | Add complete limit, isolation, reset, snapshot, and concurrency coverage. |
| `starter_kit/starter_kit/tests/test_app.py` | Modify | Add top-selection, complete shape, empty/no-overlap, exact boundary, and safe-page contract coverage. |
| `starter_kit/starter_kit/NOTAS.md` | Create | Maintain honest identity/timing/status, decisions, bounded notes, legacy defect table, AI disclosure, ledger summary, screenshot, and one-week follow-up. |
| `starter_kit/starter_kit/evidence/protected_baseline.json` | Create | Pre-edit file hashes and canonical `INTENTS` hash used by delivery verification. |
| `starter_kit/starter_kit/evidence/pending_source_corrections.jsonl` | Create | Durable generated pending records; contains no automatic correction and remains reviewable. |
| `starter_kit/starter_kit/evidence/enterprise-abstention.png` | Create | Final runtime screenshot of the real Enterprise question and visible SIN_EVIDENCIA abstention; never fabricated during planning. |

**Planned file count**: 9 new, 8 modified, 0 deleted. The screenshot and ledger are generated evidence but remain part of complete delivery identity; they are not a reason to compress authored code or documentation.

## Interfaces / Contracts

### Intent classifier

```python
def classify_intent(message: str | None) -> str:
    """Return an INTENTS key or UNKNOWN; never mutate the catalog."""
```

### Intent report

```python
async def count_messages_by_intent(workspace_id: str) -> dict[str, int]:
    """Return all active intent counts plus desconocido; propagate KeyError."""
```

The count sum equals the number of retrieved workspace messages. Any classifier value outside the active database set increments `desconocido`.

### Pending correction ledger

```python
class PendingCorrection(TypedDict):
    schema_version: int
    status: Literal["pending"]
    workspace_id: str
    answer_id: str
    source_id: str | None
    reason: Literal["missing_source", "malformed_source", "missing_title"]
    detail: str
    first_observed_at: str

class PendingCorrectionLedger:
    def __init__(self, path: Path) -> None: ...
    def record(self, correction: PendingCorrection) -> None: ...
    def pending(self) -> list[PendingCorrection]: ...

async def get_workspace_answers(
    workspace_id: str,
    min_similitud: float = 0.0,
    *,
    ledger: PendingCorrectionLedger = DEFAULT_LEDGER,
) -> list[dict]: ...
```

The legacy returned-answer dictionary remains the current schema: original answer fields plus `fuente_titulo` and `confianza`; it receives no unavailable/status marker. `answer_id` is obtained from `Record.id` for ledger records, not injected into returned data unless already present.

### Query pipeline

```python
async def consultar(pregunta: str, workspace_id: str = "acme") -> dict:
    return {
        "pregunta": pregunta,
        "workspace": workspace_id,
        "intencion": str,
        "especialista": str | None,
        "fragmentos": list[dict],
        "veredicto": "APROBADO" | "DUDOSO" | "SIN_EVIDENCIA",
        "motivo": str,
        "respuesta": str | None,
    }
```

No fragments are discarded. `motivo` includes the observed top score and relevant threshold, or explicitly states that no fragments exist.

### Loop guard

```python
class LoopGuard:
    def __init__(self, max_calls: int = MAX_CALLS): ...
    def record(self, session_id: str, agent_name: str) -> int: ...
    def reset(self, session_id: str) -> None: ...
    def snapshot(self, session_id: str) -> dict[str, int]: ...
```

For `MAX_CALLS == 3`, records 1, 2, and 3 succeed; attempted record 4 raises with attempted count 4 and limit 3, while the stored snapshot remains 3.

### Delivery verifier

```text
python -m tools.verify_delivery

Exit 0: protected files/catalog/dependencies match; ledger is parseable.
Exit nonzero: integrity mismatch, dependency expansion, or malformed ledger.
Output always: every pending correction, or "0 unresolved pending corrections".
```

A non-empty valid pending ledger is surfaced as unresolved evidence, not misreported as corruption or silently corrected.

## Testing Strategy

Strict TDD mode is disabled because the workspace root has no explicit command covering all in-scope projects. Implementation still uses ordinary task-level RED/GREEN checks: add the focused failing test for each behavior, implement the behavior, run the focused command, then run the available full suite and record honest remaining failures until final integration.

The isolated interpreter is `/home/jero/Documentos/VentureLogic_Test/.venv/bin/python`. Commands run from `starter_kit/starter_kit`; the full command is `/home/jero/Documentos/VentureLogic_Test/.venv/bin/python -m pytest`. The observed baseline is 21 collected and 21 expected `NotImplementedError` failures, with zero environment/setup failures.

| Layer | What to test | Approach |
|---|---|---|
| Unit | Classifier normalization, quote exclusion, minimum length, longest/tie behavior | Run the unchanged protected classifier file; never edit its 18 cases or `INTENTS`. |
| Unit | Intent report active/zero/unknown/error semantics | Async tests with supplied fixtures and patched unsupported classifier results; verify exact totals and singleton instantiation counts across repeated calls. |
| Unit | Legacy threshold, isolation, batching, and omission policy | Synthetic singleton-backed data and injectable `tmp_path` ledger; instrument source table reads to prove one batch; mutate one result and prove later/concurrent results are unaffected. |
| Unit | Invalid-source audit | Separate missing, malformed, and title-less cases; assert valid answers remain, invalid answers are absent, reason codes/identifiers are distinct, logs exist, and protected data is unchanged. |
| Unit | LoopGuard concurrency and ownership | Test calls through limit and MAX+1, two sessions/agents, unknown reset, snapshot mutation, and many same-key records via `ThreadPoolExecutor` with a high configured limit. |
| Unit | `consultar()` contract and boundaries | Patch `search()` with unsorted/multiple fragments and exact scores `0.549999`, `0.55`, `0.749999`, and `0.75`; assert all fragments, true maximum selection, response text identity, verdict, and numeric reason. |
| Integration | Singleton pipeline behavior | Exercise report and retriever repeatedly in one process; assert `_INSTANTIATIONS` stays one per client after first acquisition. |
| Integration | Safe HTTP/browser adapter | Request page/API locally; submit `<img onerror=...>`/`<script>` question and fixture-shaped text, confirm no `innerHTML` data sink and inspect that text appears inert; verify all fragments/scores and selected marker are visible. |
| Contract/document | Verifier v2 | Parse sample output as JSON, inspect required/closed keys, confirm no rewritten-answer field, and reconcile a-1…a-5 against fixture source ownership, literal text, chunk metadata, and scores. |
| Delivery | Protected/dependency integrity and ledger | Run `python -m tools.verify_delivery`; compare the canonical catalog and every protected hash, then enumerate all pending records or explicit zero. |
| E2E | Local console outcomes | Start `python app.py`; verify the supplied APROBADO, DUDOSO, and Enterprise SIN_EVIDENCIA questions at `http://localhost:8000`; capture only the actual Enterprise abstention. |
| Reproducibility | Fresh-clone delivery | Clone the delivered local revision into a clean sibling directory, install/use only declared requirements, run full pytest and verifier, start the server without network/credentials, record revision/timestamps/outcomes in `NOTAS.md`, and retain any failure honestly. |

Every work unit records its focused command and exact result, runtime scenario/result or explicit N/A, and rollback boundary. Final success requires the full suite to pass; intermediate full-suite placeholder failures remain documented rather than hidden.

## Threat Matrix

The design includes an HTTP/process boundary for the local console and a manual fresh-clone/startup verification step, so the applicability matrix was reviewed. It introduces no command router, executable-file classifier, Git/PR automation, or subprocess wrapper; therefore every matrix row is explicitly N/A. Browser injection and startup behavior are covered in the testing strategy above rather than forcing unrelated VCS RED tests.

| Boundary | Minimum adversarial cases | Applicability | Design response | Planned RED tests |
|---|---|---|---|---|
| Documentation-like paths | `requirements.txt`, `CMakeLists.txt`, executable Markdown/MDX, `README.sh` | N/A — no executable-file classification or command dispatch is added. | Protected declarations are hashed as data; none are executed based on filename. | None; safe-rendering tests cover the actual untrusted-text boundary. |
| Git repository selection | `git -C`, relative paths, absolute paths | N/A — application and verification code do not select or invoke Git repositories. | Fresh-clone setup is a human-run delivery procedure outside runtime code. | None. |
| Commit state | staged, `commit -a`, empty index | N/A — no commit automation is implemented. | Commit/line evidence is inspected manually per review slice. | None. |
| Push state | tracking branch, first push, explicit refspec | N/A — no push automation is implemented or authorized. | Chain design specifies review bases only; it performs no remote operation. | None. |
| PR commands | explicit `--head`, environment prefix, composed commands | N/A — no PR command construction or execution is implemented. | PR creation remains outside this design phase and requires normal authorization. | None. |

## Review Work Units and Auto-Chain

**Strategy**: Feature Branch Chain with a draft/no-merge tracker. This design defines boundaries only; it creates no tasks, branches, commits, or PRs.

**Baseline prerequisite**: Because the repository has no commits and all supplied files are untracked, preserve the supplied assessment as an explicit provenance baseline before feature edits. If that initial imported baseline itself must be reviewed as a PR, it is an unsplittable supplied-input exception and must be labeled honestly; its lines are not authored feature work. Feature line budgets begin from that immutable baseline.

```text
baseline
  └── tracker: feat/complete-technical-assessment
       └── 01 classifier + initial notes/baseline manifest
            └── 02 intent report
                 └── 03 consultar core
                      └── 04 safe console
                           └── 05 legacy retrieval + correction ledger
                                └── 06 verifier v2 + fixture matrix
                                     └── 07 LoopGuard
                                          └── 08 final audit + fresh-clone evidence
```

| Slice | Deliverable boundary | Dependencies | Included verification/docs | Forecast authored lines | Rollback boundary |
|---|---|---|---|---:|---|
| 01 | Deterministic classifier and pre-edit integrity baseline | Supplied baseline | Protected classifier tests; create incomplete `NOTAS.md`; baseline hashes | 180–280 | Revert classifier implementation, initial notes, and manifest together. |
| 02 | Active-intent coverage report | 01 classifier | Expanded report tests; report decision note | 120–200 | Revert report module/tests/note only. |
| 03 | Async `consultar()` evidence core | 01 classifier | Exact shape, top-fragment, empty, and 0.55/0.75 boundary tests; threshold note | 170–270 | Revert orchestration/tests without touching HTTP shell. |
| 04 | Safe human-readable console | 03 core | Text-sink contract tests and manual inert-markup smoke; notes update | 180–300 | Restore prior page while retaining tested `consultar()`. |
| 05 | Isolated legacy retrieval and durable omission ledger | Baseline clients | Correction ledger, legacy tests, one-batch proof, defect table update | 300–400 | Revert legacy module, ledger module/data, tests, and corresponding notes. |
| 06 | Strict verifier v2 and expected fixture matrix | Shared thresholds/source policy | JSON contract inspection and bounded verifier note | 140–240 | Remove v2/matrix and note while preserving v1. |
| 07 | Thread-safe LoopGuard | None beyond stdlib | Full loop-guard suite and interception-point note | 140–230 | Revert guard/tests/note only. |
| 08 | Delivery verifier and truthful final evidence | 01–07 | Integrity/dependency/ledger report, screenshot, full suite, fresh-clone startup, final notes | 180–300 plus generated screenshot | Revert final audit tooling/evidence updates without altering capabilities. |

Each slice targets its immediate predecessor and must expose only its own diff. If measured authored additions plus deletions exceed 400, perform one honest split by behavior (for example, separate slice 05 into ledger infrastructure and legacy integration only if both remain coherent and independently verified). If no cohesive split fits after that one pass, report the smallest honest count and request `size:exception`; do not code-golf tests or documentation. Generated screenshot bytes and generated ledger lines are excluded from authored risk count but included in revision identity and receipts.

## Migration / Rollout

No application data migration is required. The correction ledger starts at schema version 1 and may be absent/empty before the first invalid-source omission; verification reports zero in that state. Existing valid answer consumers see the same list/dictionary schema.

Rollout is local and dependency-first through the chain. The tracker remains no-merge until all child slices, the full suite, protected/dependency audit, ledger review, and fresh-clone console smoke succeed. Invalid-source records remain pending. Any source/fixture/data correction in the final phase is a separate, explicit user-authorization gate; without authorization, delivery keeps omissions, ledger evidence, and protected data unchanged.

## Open Questions

- Candidate name, actual start/delivery timestamps, real hours per exercise, exact AI-use disclosure, final completion status, and screenshot provenance must be supplied from real activity; placeholders remain visibly incomplete until then.
- The assessment's 72-hour cover statement conflicts with its page-2 no-deadline statement and still requires assessor clarification; it does not block implementation.
- During the final phase, the user must explicitly decide whether any ledger-listed source/fixture/data defects may be corrected. The default is no correction.

None of these questions blocks the implementation design.
