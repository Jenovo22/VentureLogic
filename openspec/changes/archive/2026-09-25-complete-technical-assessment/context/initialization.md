**What**: Refreshed the authoritative SDD project context using Engram persistence without modifying the native control-plane declaration or creating OpenSpec planning artifacts.
**Why**: The runtime requested a fresh, evidence-backed initialization before any assessment implementation.
**Where**: `/home/jero/Documentos/VentureLogic_Test`; discovered project `starter_kit/starter_kit`; bounded input `02_Prueba_Practica.pdf`; read-only control declaration `openspec/config.yaml`.
**Learned**: The workspace is now an initialized Git worktree on unborn branch `master`, unlike the prior refresh; every file is untracked and there are no commits. CodeGraph lazy initialization was attempted once but failed because the upstream `codegraph` executable is unavailable.

## Project Context

- Project: `venturelogic_test`
- Authoritative workspace: `/home/jero/Documentos/VentureLogic_Test`
- Persistence: Engram. `openspec/config.yaml` contains only `sdd.artifact_store: engram`; it was not modified, and no proposal/change/planning artifacts were created.
- Pace: interactive
- Delivery strategy: auto-chain
- Review policy: 400 authored changed lines per PR
- Git: repository detected; branch `master`; no commits; all workspace inputs are untracked.

## Bounded Workspace Discovery

| Relative path | Role | Evidence |
| --- | --- | --- |
| `.` | Authoritative workspace/container root | Git metadata, assessment PDF, `starter_kit/`, `.atl/`, and the native `openspec/config.yaml` declaration; no project manifest, CI, Makefile, or root test target. |
| `starter_kit/starter_kit` | Only discovered project root | `pytest.ini`, `requirements.txt`, Python modules, deterministic fixtures, and pytest tests. |
| `starter_kit/__MACOSX` | Excluded packaging metadata | Finder resource-fork files only; not a project. |
| `02_Prueba_Practica.pdf` | Bounded assessment context | Six exercises, acceptance criteria, protected files, local pytest flow, no-new-dependency restriction, required `NOTAS.md`, and real incremental commits. |

## Stack and Architecture

- Python 3.10+; host `python3` is 3.12.3; `python` is absent.
- Application code uses the standard library (`asyncio`, `http.server`, JSON, logging, pathlib); development requirements declare `pytest>=8.0` and `pytest-asyncio>=0.23`.
- Pipeline architecture: intent classifier -> lexical retriever -> specialist routing -> evidence verdict -> final response; the current starter remains intentionally unimplemented in exercises 1, 2, 5, and 6.
- `app.py` is a thin stdlib HTTP adapter around directly testable async `consultar()`.
- `config/` owns intent/routing policy; `shared/` owns singleton adapters and retrieval; `tools/` owns focused async tools; `fixtures/` provides deterministic local data; `tests/` defines pytest contracts.
- Shared clients are process-level singletons. Tool code must call `get_db_client()` and `get_storage_client()` rather than instantiate clients.

## Conventions and Constraints

- Existing source and docs use Spanish domain names/docstrings, type hints, async I/O boundaries, module logging, and deterministic fixtures.
- Protected from modification: `shared/clients.py`, `shared/retriever.py`, `fixtures/`, `pytest.ini`, and `tests/test_classify_intent.py`.
- No dependencies may be added. Delivery requires `NOTAS.md`, disclosure of AI usage, a screenshot for the Enterprise abstention case, and small real commits.
- CodeGraph fallback evidence: `gentle-ai codegraph init --cwd /home/jero/Documentos/VentureLogic_Test` failed with `exec: "codegraph": executable file not found in $PATH`; structural inspection therefore used bounded filesystem reads.

## Strict TDD

Strict TDD is disabled. There is one non-empty discovered project and its local command is `pytest` from `starter_kit/starter_kit`, but the authoritative workspace root defines no explicit workspace-level command covering every in-scope project. No explicit `strict_tdd` marker is present. SDD therefore fails closed and does not synthesize a root command from the project-local command.
