## Capability: assistant-console

# Assistant Console Specification

## Purpose

Define separately testable assistant orchestration and a safe, local, dependency-free evidence console.

## Requirements

### Requirement: Orchestrate the Complete Query Pipeline

`consultar()` MUST classify the question, resolve the configured specialist, retrieve evidence asynchronously, preserve every returned fragment, select the highest-scoring fragment, and return the documented result fields.

#### Scenario: Evidence is retrieved
- GIVEN a valid question with multiple retrieved fragments
- WHEN `consultar()` runs
- THEN the result MUST expose the classified intent, selected specialist, all fragments and scores, top evidence, verdict, reason, and response
- AND the top evidence MUST have the highest observed score

#### Scenario: Retriever returns no fragments
- GIVEN a valid question for which retrieval returns no fragments
- WHEN `consultar()` runs
- THEN every returned fragment collection MUST be empty
- AND the verdict MUST be `SIN_EVIDENCIA`
- AND `respuesta` MUST be `None`

### Requirement: Apply Exact Verdict Boundaries

The pipeline MUST return `SIN_EVIDENCIA` below `0.55`, `DUDOSO` from `0.55` inclusive to below `0.75`, and `APROBADO` at or above `0.75`; every reason MUST cite the observed score or absence and applicable threshold.

#### Scenario: Below minimum evidence
- GIVEN the top score is `0.549999`
- WHEN `consultar()` evaluates it
- THEN the verdict MUST be `SIN_EVIDENCIA`
- AND `respuesta` MUST be `None`

#### Scenario: Doubt boundaries
- GIVEN top scores of exactly `0.55` and `0.749999` in separate requests
- WHEN each request is evaluated
- THEN both verdicts MUST be `DUDOSO`
- AND each response MUST contain the top fragment text

#### Scenario: Approval boundary
- GIVEN the top score is exactly `0.75`
- WHEN `consultar()` evaluates it
- THEN the verdict MUST be `APROBADO`
- AND the response MUST contain the top fragment text

### Requirement: Abstain Explicitly Without Rewriting Evidence

The assistant MUST visibly abstain when evidence is absent or below minimum and MUST use retrieved fragment text, without inventing or rewriting an answer, for doubtful and approved outcomes.

#### Scenario: Enterprise-plan question lacks evidence
- GIVEN the mandated Enterprise-plan question produces a top score below `0.55`
- WHEN it is submitted
- THEN the user MUST see `SIN_EVIDENCIA` and an explicit abstention
- AND no unsupported plan answer MUST be displayed

#### Scenario: Doubtful evidence is shown transparently
- GIVEN usable evidence scores between the two thresholds
- WHEN it is submitted
- THEN the fragment text MUST remain available
- AND the console MUST visibly distinguish `DUDOSO` from approval

### Requirement: Render Complete Evidence Safely

The local console MUST display intent, specialist, every fragment and score, verdict, reason, and response or explicit abstention, and MUST render all question and fixture-derived values as text rather than executable markup.

#### Scenario: Untrusted markup is submitted
- GIVEN a question or fixture fragment contains HTML or script syntax
- WHEN the console renders the result
- THEN the syntax MUST be displayed as inert text
- AND it MUST NOT execute or create active markup

#### Scenario: Multiple fragments are visible
- GIVEN retrieval returns multiple fragments
- WHEN the result is rendered
- THEN every fragment and corresponding score MUST be inspectable
- AND the selected top fragment MUST be distinguishable

### Requirement: Run Locally Without External Services

The console MUST run with the supplied dependency set at `http://localhost:8000` and MUST require no network access, credentials, framework, or external service.

#### Scenario: Fresh local startup
- GIVEN a fresh clone with only declared requirements available
- WHEN `python app.py` is started from the project directory
- THEN the console MUST serve at `http://localhost:8000`
- AND the three mandated demo questions MUST yield visible `APROBADO`, `DUDOSO`, and `SIN_EVIDENCIA` outcomes

#### Scenario: External services are unavailable
- GIVEN outbound network access and credentials are unavailable
- WHEN the console handles fixture-backed questions
- THEN classification, retrieval, verdict, and rendering MUST remain functional

---
