## Capability: assessment-delivery-compliance

# Assessment Delivery Compliance Specification

## Purpose

Define auditable constraints and truthful evidence for delivering all six assessment exercises.

## Requirements

### Requirement: Preserve Protected Inputs and Dependency Set

Delivery MUST keep `shared/clients.py`, `shared/retriever.py`, every file under `fixtures/`, `pytest.ini`, and `tests/test_classify_intent.py` byte-for-byte unchanged and MUST NOT add or expand runtime or development dependencies.

#### Scenario: Protected-file audit passes
- GIVEN the supplied baseline and final delivery
- WHEN protected paths are compared byte-for-byte
- THEN every protected file MUST be unchanged

#### Scenario: Dependency audit passes
- GIVEN the supplied and final dependency declarations
- WHEN they are compared
- THEN no package or version requirement MUST have been added or expanded
- AND runtime capabilities MUST remain dependency-free beyond the supplied standard-library design

### Requirement: Provide Rubric-Aligned Automated and Audit Evidence

Delivery MUST include focused automated tests for intent reporting, legacy retrieval, loop protection, and assistant orchestration, MUST retain protected tests, and MUST test exact threshold and call-limit boundaries. Delivery verification MUST inspect the pending-correction ledger, report every unresolved invalid-source record honestly, and expose source, fixture, or data remediation as a final-phase decision requiring explicit user authorization rather than silently applying a correction.

#### Scenario: Required behavioral coverage exists
- GIVEN the final test suite
- WHEN its cases are inspected and run
- THEN it MUST cover mixed and empty intent reports, inactive and missing workspaces, singleton reuse, legacy contamination, omission, and pending-correction recording for missing, malformed, and title-less sources, loop limit/isolation/reset/concurrency/snapshots, and assistant doubt/empty/no-overlap/boundaries

#### Scenario: Protected classifier suite passes
- GIVEN the unchanged protected classifier test file
- WHEN the declared pytest suite runs
- THEN all 18 classifier cases MUST pass
- AND no test MUST depend on network access or credentials

#### Scenario: Unresolved invalid-source records are reported
- GIVEN the pending-correction ledger contains one or more unresolved invalid-source records
- WHEN delivery verification and final-phase review are performed
- THEN the evidence MUST enumerate each unresolved record with enough answer and source identifiers and reason detail to diagnose and specify a correction
- AND verification MUST NOT report those records as corrected or omit them from the final review evidence
- AND the final phase MUST present correction as conditional on explicit user authorization at that time
- AND recording or reviewing the evidence MUST NOT modify protected sources, fixtures, or data

#### Scenario: No invalid-source omissions are recorded
- GIVEN legacy retrieval has produced no invalid-source omission records
- WHEN delivery verification inspects the pending-correction ledger
- THEN verification MUST report that the ledger contains zero unresolved records
- AND it MUST NOT fabricate a correction decision or remediation evidence

### Requirement: Maintain Truthful Submission Notes

`NOTAS.md` MUST contain candidate-provided identity, actual start and delivery timestamps, real hours per exercise, completed/incomplete status, three high-confidence decisions, two low-confidence decisions with reversal evidence, the required bounded conceptual notes, the legacy defect table, exact AI-use disclosure, and the one-week follow-up.

#### Scenario: Facts are not yet available
- GIVEN identity, timestamps, hours, AI usage, or completion facts have not yet occurred or been supplied
- WHEN notes are updated
- THEN placeholders MUST be explicitly marked incomplete
- AND fabricated names, times, hours, disclosures, or completion claims MUST NOT be recorded

#### Scenario: Final notes are auditable
- GIVEN implementation and verification activity has occurred
- WHEN `NOTAS.md` is finalized
- THEN each factual field MUST reflect actual activity
- AND every bounded note MUST remain within its PDF-defined word limit
- AND each legacy defect row MUST state location, problem, concrete production symptom, and severity

### Requirement: Capture Genuine Abstention Evidence

The final notes MUST include a screenshot from the actual running console showing the Enterprise-plan question and visible abstention, and MUST identify enough runtime context to associate it with the delivered revision.

#### Scenario: Required screenshot is captured
- GIVEN the final delivered revision is running locally
- WHEN the Enterprise-plan question is submitted
- THEN the captured screenshot MUST show the question and `SIN_EVIDENCIA` abstention
- AND it MUST be embedded or referenced by `NOTAS.md`

#### Scenario: Screenshot is unavailable before implementation
- GIVEN the final console has not run yet
- WHEN planning artifacts are produced
- THEN no screenshot MUST be fabricated or substituted
- AND the evidence item MUST remain explicitly pending

### Requirement: Preserve Incremental and Reviewable Delivery History

Delivery MUST use multiple coherent commits and autonomous review slices; under `auto-chain`, any slice approaching or exceeding 400 authored changed lines MUST be split, and each child review MUST expose only its own changes against the immediately preceding slice.

#### Scenario: Slice remains within budget
- GIVEN a proposed review slice
- WHEN authored additions plus deletions are measured
- THEN the slice MUST contain no more than 400 authored changed lines
- OR it MUST be split before review

#### Scenario: Chained review remains isolated
- GIVEN a child slice follows an earlier slice
- WHEN its review diff is inspected
- THEN its base MUST be the immediately preceding slice
- AND previously reviewed changes MUST NOT appear as new child changes
- AND generated evidence MAY be excluded from authored risk count but MUST remain identifiable in delivery receipts

### Requirement: Verify Reproducibility from a Fresh Clone

Before submission, the delivered revision MUST be verified from a fresh clone by running the declared pytest suite and serving `python app.py` at `http://localhost:8000` without network access or credentials; actual commands, revision, timestamps, and outcomes MUST be recorded truthfully.

#### Scenario: Fresh-clone verification succeeds
- GIVEN a fresh clone of the delivered revision with declared requirements available
- WHEN the declared tests run and the application starts
- THEN the full suite MUST pass
- AND the local console MUST respond at the required URL without external access
- AND the evidence record MUST identify the verified revision and actual outcomes

#### Scenario: Verification fails
- GIVEN any test or startup check fails
- WHEN delivery evidence is recorded
- THEN the failure MUST remain visible and the delivery MUST NOT claim completion
- AND corrective work MUST preserve protected files and dependency restrictions
