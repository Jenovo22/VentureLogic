# OpenSpec storage migration

This is a user-authorized, content-preserving storage migration on 2026-09-24 for project `venturelogic_test`, change `complete-technical-assessment`. It is not a new SDD phase, implementation plan, implementation attempt, or grant for future task execution. Engram history remains untouched; its write/session-registration failures are the reason for this migration. The memory mirror is unavailable and was not retried.

## Current context and authority

- Preserve the latest selections: **Interactive**, **Auto** (`auto-chain`), **feature-branch-chain**. The historical single-PR exception is not active policy.
- The authorized edit root for this migration is `/home/jero/Documentos/VentureLogic_Test`. Only OpenSpec planning/configuration files are changed. No commits, branch changes, remote actions, installations, source/test/fixture changes, feature design, or task execution are authorized by this migration.
- Current environment supplied by the user: workspace `.venv`, Python 3.12.3, installed pytest 9.1.1 and pytest-asyncio 1.4.0; previously observed baseline: 21 `NotImplementedError` failures. These are carried-forward observations, **not a migration retest**. No test suite or application was run during migration.
- The environment and persistence statements in `exploration.md`, `proposal.md`, `context/initialization.md`, and `context/testing-capabilities.md` are **historical source facts**, not current environment guidance. Their older missing-pytest/Engram-only statements are preserved verbatim for provenance. The proposal's exclusion of OpenSpec planning files describes the original Engram-backed phase; the user's explicit storage-migration authorization supersedes that storage restriction for this bounded operation only.
- `context/legacy-source-policy.md` remains applicable: invalid-source answers are omitted and recorded; remediation of protected sources, fixtures, or data still requires explicit later user authorization.
- Local context files are references, not dispatch artifacts. Future phases should read this record and the local context references alongside the native-resolved proposal/specs/design/tasks; no Engram write or read is needed to recover the migrated context.

## Source-to-target provenance

All nine observations were retrieved in full with `mem_get_observation`. Revisions and created timestamps below are the values observed in its metadata; no unexposed revision timestamp is inferred. Target paths are relative to this change directory. Topic prefix `change/` below means `sdd/complete-technical-assessment/`.

| Observation | Revision | Topic | Created (as reported) | Target |
|---|---:|---|---|---|
| 13 | 1 | `change/explore` | 2026-09-24 11:20:49 | `exploration.md` |
| 15 | 1 | `change/proposal` | 2026-09-24 11:30:23 | `proposal.md` |
| 16 | 4 | `change/spec` | 2026-09-24 11:35:15 | Seven `specs/<capability>/spec.md` files below and `context/spec-notes.md` |
| 20 | 1 | `change/design` | 2026-09-24 11:57:09 | `design.md` |
| 22 | 2 | `change/tasks` | 2026-09-24 13:36:13 | `tasks.md` |
| 5 | 2 | `sdd-init/venturelogic_test` | 2026-09-24 11:04:45 | `context/initialization.md` |
| 6 | 2 | `sdd/venturelogic_test/testing-capabilities` | 2026-09-24 11:04:45 | `context/testing-capabilities.md` |
| 17 | 2 | `change/legacy-source-policy` | 2026-09-24 11:36:48 | `context/legacy-source-policy.md` |
| 21 | 1 | `change/chain-strategy` | 2026-09-24 12:01:31 | `context/chain-strategy.md` |

## Preservation evidence

Before migration, `openspec/` contained only `config.yaml` with `sdd.artifact_store: engram`; no target artifact collision existed. Every migrated file was read back completely by the read-only comparison. Source extraction removed only the MCP observation heading and the metadata footer beginning with `Session:`. Markdown content was not summarized, reformatted, or truncated.

Eight one-to-one copies passed exact UTF-8 comparison against the full source content plus one terminal LF for Markdown-file serialization. Source contents themselves were preserved exactly; no whitespace normalization or content trimming was used. The SHA-256 values below identify the resulting file bytes.

| Target | Bytes | SHA-256 |
|---|---:|---|
| `exploration.md` | 14344 | `59e75857821735f503c057fc49016e53a93e513c15a8a71a94311fcf30becfaf` |
| `proposal.md` | 14621 | `35cc4e76330ecc4a36ebdc65c05c0a7836193253a1b7241a4be3cc15b1928372` |
| `design.md` | 34566 | `53b8148331074affd70f230ff8e71ddd4f1563a7fee61f3c9c87cf8c2e2fbe49` |
| `tasks.md` | 17153 | `d7c4cea7b06360747c1f92a757c2c5d79283f8cb3bf0f56a5c012d4a548dfd2f` |
| `context/initialization.md` | 4052 | `3eb081470280104f4c93392cd12964675b97a02164b2c5777b763529514221f8` |
| `context/testing-capabilities.md` | 2931 | `d57ea562e7e423970cb257122288053005a7bb77ab8a41d86c1eb5f9cee164d3` |
| `context/legacy-source-policy.md` | 760 | `2bacac8a5c03c01896b61758a4c86920461f8bf292e760bf8ff4c394c77797c3` |
| `context/chain-strategy.md` | 504 | `6893573c8123da2045e73458122c2abe4a6833e389f9b100efc0ff08ea0127e2` |

Observation 16 was split at its seven existing `## Capability:` headings without modifying requirement/scenario blocks. Existing inter-capability `---` separators remain at the ends of the first six files. One boundary blank line is restored when joining each file for reconstruction. `context/spec-notes.md` holds the original consolidated title followed by the complete trailing `## Cross-Capability Unresolved Decision` section. Reconstructing title + seven files in source order + trailing notes exactly matches the complete source plus a terminal LF: SHA-256 `7fcfafb7c18e42fe3d75fd08f2fa3b79b0f42e4e83e9365acfcdb84f6781a7da`.

| Capability (source order) | Requirements | Scenarios | Spec file SHA-256 |
|---|---:|---:|---|
| `intent-classification` | 4 | 8 | `a30e91ac897804a7e7dafb4dff449990f8fbe07f38c08840271cb60ecc861a43` |
| `intent-coverage-reporting` | 4 | 8 | `96a2d611d7dc324a5e5fedc20d8243dae8e665f035d2f0460ff9a1c3f451086f` |
| `legacy-answer-retrieval` | 4 | 9 | `90a0b006ee3008f4463afca899139bc58dcc502d270d9532f8c199d1c0315175` |
| `evidence-verification` | 5 | 10 | `463edce04952bc1cd0887b8a46afd93a59c2b293d3531b680c93a58f41d7b71b` |
| `tool-loop-protection` | 4 | 8 | `e349cbdb64f64f0069214a4e11a251805b2c9130cec6ee908911f5184dc7db53` |
| `assistant-console` | 5 | 11 | `091c541d4106f4feb68f996c2e67697cdde3d1d229469020730abeb45d79651e` |
| `assessment-delivery-compliance` | 6 | 14 | `7fd689d39f33fdd60a5ff53d0aaf0a0f988ec728311a84c1ed1b0fe8920c5c28` |
| **Total** | **32** | **68** | Every source requirement/scenario occurs exactly once across these seven files. |

Task IDs and unchecked states are unchanged: `0.1, 0.2, 1.1–1.4, 2.1–2.3, 3.1–3.3, 4.1–4.3, 5.1–5.4, 6.1–6.3, 7.1–7.2, 8.1–8.4`: **28 total, 0 completed, 28 pending**. No apply-progress artifact, phase attempt, readiness receipt, or verification report was fabricated.

## Native verification

Command (read-only; does not launch a phase):

```sh
gentle-ai sdd-status complete-technical-assessment --cwd "/home/jero/Documentos/VentureLogic_Test" --json --instructions
```

Pre-migration native result: `artifactStore: engram`, exact change selected, proposal/specs/design/tasks `done`, `applyState: ready`, task progress 28/0/28, apply-progress absent, and workspace-only allowed edit roots.

Post-switch command exited successfully. The complete returned JSON is preserved in `context/migration-status.json`. It reports `schemaName: gentle-ai.sdd-status`, `schemaVersion: 2`, `changeName: complete-technical-assessment`, `artifactStore: openspec`, proposal/specs/design/tasks `done`, `applyState: ready`, task progress `{total: 28, completed: 0, pending: 28, allComplete: false}`, `nextRecommended: apply`, and `blockedReasons: []`. All primary artifact locators resolve to the new local files; apply-progress and verify-report remain missing. The allowed edit roots remain exactly `[/home/jero/Documentos/VentureLogic_Test]`. The informational `/tmp` warning is unchanged.

Only the supported `sdd.artifact_store` declaration changed, from `engram` to `openspec`, after artifact readback/preservation checks. Native status required no additional change metadata or marker for this workspace-local change, so none was invented. No `state.yaml`, phase attempt, or receipt was synthesized. The native recommendation is recorded, not executed.

## Remaining warnings

- Native status reports: `note(future_edit_roots): a later work unit in tasks.md targets edit paths outside the authorized edit roots: "/tmp"; this does not block the current work unit and needs no action until that work unit is reached`. The task content is preserved; this migration neither fixes nor conceals the warning and grants no `/tmp` edit authority.
- Preserved planning text includes historical environment/storage facts, unresolved candidate/timing/screenshot facts, and the assessment's deadline ambiguity. Migration does not resolve product or delivery questions.
- Engram memory mirror unavailable: discoveries and this session's migration outcome are recorded locally here instead. No session ID was invented or registered and no Engram mutation was attempted.

## Skill resolution

Read before work: `/home/jero/.config/opencode/skills/cognitive-doc-design/SKILL.md` and `/home/jero/.config/opencode/skills/_shared/openspec-convention.md`. Also read the installed `_shared/sdd-status-contract.md` for native status/authority behavior. Cognitive-document guidance applies only to this provenance record; migrated artifacts retain their original organization and wording. No SDD phase or implementation skill was executed.
