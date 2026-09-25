## Capability: evidence-verification

# Evidence Verification Specification

## Purpose

Define a strict verifier v2 contract and deterministic fixture verdicts while preserving the v1 baseline.

## Requirements

### Requirement: Require Authoritative Evidence Inputs

Verifier v2 MUST receive the candidate answer, claimed citation, similarity score, and authoritative retrieved evidence including valid source and chunk traceability metadata.

#### Scenario: Complete evidence input
- GIVEN an answer includes a claimed literal citation and authoritative source and chunk metadata
- WHEN verification begins
- THEN literalness, source validity, traceability, and similarity MUST all be evaluated

#### Scenario: Authoritative evidence is unavailable
- GIVEN the verifier cannot compare the claim with authoritative retrieved evidence
- WHEN verification is requested
- THEN the answer MUST NOT be approved
- AND the result MUST state that evidence validity could not be established

### Requirement: Validate Literal Citation and Source Identity

The verifier MUST reject generic paraphrases presented as citations and MUST reject nonexistent or mismatched source references before considering a doubtful verdict.

#### Scenario: Literal citation has valid source
- GIVEN the claimed citation occurs literally in the authoritative fragment and its source identifier is valid
- WHEN verification is performed
- THEN the citation and source checks MUST pass

#### Scenario: Plausible text references invalid source
- GIVEN the answer text is plausible but the claimed source identifier is nonexistent or does not own the fragment
- WHEN verification is performed
- THEN the verdict MUST be `RECHAZADO`

### Requirement: Apply Aligned Evidence Thresholds

The verifier MUST use `0.55` as minimum usable evidence and `0.75` as the approval threshold. Scores below `0.55` MUST be rejected; valid evidence from `0.55` to below `0.75` MUST NOT be approved; and complete valid evidence at or above `0.75` MAY be approved.

#### Scenario: Score below minimum
- GIVEN otherwise plausible evidence has similarity `0.549999`
- WHEN verification is performed
- THEN the verdict MUST be `RECHAZADO`

#### Scenario: Exact boundaries
- GIVEN complete valid evidence is verified at `0.55` and at `0.75`
- WHEN each case is evaluated
- THEN `0.55` MUST NOT produce `APROBADO`
- AND `0.75` MAY produce `APROBADO` when every other check passes

### Requirement: Distinguish Incomplete Traceability

Usable, literal, valid-source evidence at or above `0.55` but lacking required traceability metadata MUST produce `DUDOSO` rather than `APROBADO`; an invalid source MUST remain `RECHAZADO`.

#### Scenario: Valid evidence lacks chunk metadata
- GIVEN a literal citation with a valid source scores `0.86` but required chunk metadata is missing
- WHEN verification is performed
- THEN the verdict MUST be `DUDOSO`
- AND the reason MUST identify the missing traceability field

#### Scenario: Missing metadata does not rescue invalid source
- GIVEN evidence lacks chunk metadata and references an invalid source
- WHEN verification is performed
- THEN the verdict MUST be `RECHAZADO`, not `DUDOSO`

### Requirement: Emit Strict Non-Rewriting Verdicts and Fixture Matrix

Verifier v2 MUST emit only the documented strict JSON verdict contract, MUST provide a reason grounded in observed checks, and MUST NOT rewrite or improve the candidate answer. The fixture matrix MUST preserve v1 and document deterministic expected outcomes for a-1 through a-5. For a-3, the matrix MUST require `RECHAZADO` because its claimed citation is not a literal substring of the authoritative source, despite its valid source identifier and high similarity score.

#### Scenario: Strict output contract
- GIVEN any valid verifier input
- WHEN verification completes
- THEN the output MUST be valid JSON matching the documented schema with no surrounding prose
- AND it MUST retain the candidate answer without a rewritten replacement

#### Scenario: Fixture verdict matrix
- GIVEN fixture answers a-1 through a-5
- WHEN their documented expectations are inspected
- THEN a-1 MUST be `APROBADO`, a-2 `RECHAZADO`, a-3 `RECHAZADO`, a-4 `RECHAZADO`, and a-5 `DUDOSO`
- AND the a-3 reason MUST identify that `Configuración > Equipo` is a nonliteral paraphrase of the authoritative `Configuración, luego a Equipo` wording, despite the valid `src-2` reference and `0.88` similarity
- AND each entry MUST include a one-line reason tied to literalness, source validity, similarity, or traceability

---
