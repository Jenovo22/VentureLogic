## Capability: legacy-answer-retrieval

# Legacy Answer Retrieval Specification

## Purpose

Define safe retrieval of one workspace's answers enriched with source titles while preserving request isolation and partial availability.

## Requirements

### Requirement: Return Workspace Answers with Source Titles

The tool MUST return only answers supplied for the requested workspace and MUST enrich each successfully resolved answer with the title of its referenced source while honoring `min_similitud` exactly.

#### Scenario: Valid answers are enriched
- GIVEN a workspace has answers above or equal to the requested minimum similarity and valid source records
- WHEN answers are requested
- THEN every eligible answer MUST be returned with the matching source title
- AND answers below the minimum MUST be absent

#### Scenario: Threshold boundary is inclusive
- GIVEN one answer has similarity exactly equal to `min_similitud` and another is below it
- WHEN answers are requested
- THEN the equal answer MUST be included
- AND the lower answer MUST be excluded

### Requirement: Isolate Every Request

The tool MUST return fresh request-owned data, MUST NOT reuse mutable results across requests, and MUST NOT create process-wide or shared temporary-file answer state.

#### Scenario: Consecutive workspaces do not contaminate each other
- GIVEN two workspaces have different answers
- WHEN their requests run consecutively or concurrently
- THEN each result MUST contain only its workspace's supplied answers
- AND mutation of one returned result MUST NOT alter any other result

#### Scenario: Similarity settings do not contaminate each other
- GIVEN the same workspace is requested with two different minimum similarities
- WHEN both requests complete
- THEN each result MUST independently reflect its own threshold
- AND no `/tmp/last_answers.json` or equivalent shared output MUST be created

### Requirement: Reuse Supplied Client and Avoid Per-Answer Source Reads

The tool MUST reuse the supplied database singleton and MUST resolve required source records without a sequential source read for every answer.

#### Scenario: Multiple answers reference sources
- GIVEN a workspace returns several eligible answers with repeated and distinct source identifiers
- WHEN answers are requested
- THEN the supplied singleton MUST remain the only database client instance
- AND source retrieval MUST NOT perform one sequential remote read per answer

#### Scenario: No eligible answers
- GIVEN no answer meets the requested threshold
- WHEN answers are requested
- THEN an empty fresh result MUST be returned
- AND no source retrieval MUST be required

### Requirement: Omit and Record Answers with Invalid Sources

An eligible answer whose referenced source is missing, malformed, or lacks required title data MUST be omitted from the returned result. Valid answers MUST remain available and correctly enriched, and the current enriched-answer output schema MUST NOT be expanded with an unavailable marker. Every omission MUST produce an auditable pending-correction record containing enough answer and source identifiers and reason detail to diagnose the defect and specify a correction during final-phase review. Recording an omission MUST NOT modify any protected source, fixture, or data and MUST NOT authorize remediation; any final-phase source, fixture, or data correction MUST require explicit user authorization at that time.

#### Scenario: One source is missing
- GIVEN eligible answers include one answer with a valid source and one answer with a nonexistent source
- WHEN answers are requested
- THEN the request MUST complete without a whole-request failure
- AND the valid answer MUST be returned with the matching source title
- AND the answer with the nonexistent source MUST be omitted from the returned result
- AND the pending-correction ledger MUST record the omitted answer identifier, referenced source identifier, and a reason identifying the missing source

#### Scenario: Source record is malformed or title-less
- GIVEN eligible answers include one answer with a valid source and answers whose source records are malformed or lack required title data
- WHEN answers are requested
- THEN the valid answer MUST remain available and correctly enriched
- AND every answer with a malformed or title-less source MUST be omitted from the returned result
- AND the returned enriched-answer schema MUST NOT contain an unavailable marker
- AND the pending-correction ledger MUST contain a distinct record for each omission with answer and source identifiers and a reason distinguishing malformed data from missing title data

#### Scenario: Omission evidence remains pending for final review
- GIVEN one or more invalid-source omissions have been recorded
- WHEN the pending-correction evidence is reviewed before or during the final phase
- THEN every unresolved record MUST remain auditable with its answer identifier, source identifier, and diagnostic reason
- AND the evidence MUST identify remediation as pending explicit user authorization
- AND no protected source, fixture, or data MUST be modified merely because the record exists

---
