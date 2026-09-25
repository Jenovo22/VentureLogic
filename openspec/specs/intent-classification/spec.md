## Capability: intent-classification

# Intent Classification Specification

## Purpose

Define deterministic classification of Spanish user messages against the protected intent catalog.

## Requirements

### Requirement: Normalize Eligible User Text

The classifier MUST normalize eligible user text once for case, accents including ñ, punctuation, and repeated spacing, and MUST exclude every line whose first non-spacing character is `>` before matching.

#### Scenario: Normalized message matches an intent
- GIVEN a message whose eligible text differs from a configured pattern only by case, accents, punctuation, or repeated spacing
- WHEN the message is classified
- THEN the result MUST be the intent associated with that configured pattern

#### Scenario: Quoted content is not classified
- GIVEN a message whose only matching pattern occurs on a line beginning with `>` after optional leading spacing
- WHEN the message is classified
- THEN the quoted line MUST NOT contribute to a match
- AND the result MUST be `desconocido` when no eligible line matches

### Requirement: Reject Insufficient Input

The classifier MUST return `desconocido` when the normalized eligible input is empty or shorter than the catalog contract permits.

#### Scenario: Empty input is rejected
- GIVEN an empty, punctuation-only, spacing-only, or quote-only message
- WHEN the message is classified
- THEN the result MUST be `desconocido`

#### Scenario: Short normalized input is rejected
- GIVEN a message whose normalized eligible text is below the minimum accepted length
- WHEN the message is classified
- THEN the result MUST be `desconocido` even if the text is contained within a configured pattern

### Requirement: Resolve Matches Deterministically

The classifier MUST select the longest matching configured pattern; equal-length matches MUST resolve by existing catalog order; and no match MUST return `desconocido`.

#### Scenario: Longest configured pattern wins
- GIVEN eligible text matching patterns of different lengths from multiple intents
- WHEN the message is classified
- THEN the intent owning the longest matching pattern MUST be returned

#### Scenario: Equal-length tie preserves catalog order
- GIVEN eligible text matching two equal-length configured patterns
- WHEN the message is classified repeatedly
- THEN every result MUST select the pattern appearing first in the protected catalog

### Requirement: Preserve the Protected Catalog and Generic Behavior

Classification MUST be catalog-driven, MUST NOT contain message-specific exceptions, and MUST NOT modify `INTENTS` or the protected classifier tests.

#### Scenario: Catalog additions participate without classifier changes
- GIVEN a valid intent pattern is added through an authorized catalog fixture
- WHEN matching eligible text is classified
- THEN the associated intent MUST be returned without a message-specific classifier rule

#### Scenario: Protected classifier assets remain unchanged
- GIVEN the capability has been delivered
- WHEN protected-file integrity is compared with the supplied baseline
- THEN `INTENTS` and `tests/test_classify_intent.py` MUST be byte-for-byte unchanged
- AND all 18 supplied classifier cases MUST pass

---
