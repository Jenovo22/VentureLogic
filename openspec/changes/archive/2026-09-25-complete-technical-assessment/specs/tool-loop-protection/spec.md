## Capability: tool-loop-protection

# Tool Loop Protection Specification

## Purpose

Define bounded, concurrency-safe tool-call accounting independently per session and agent.

## Requirements

### Requirement: Count Calls Per Session and Agent

The guard MUST maintain independent counts keyed by session identifier and agent name and MUST permit calls one through `MAX_CALLS` inclusive.

#### Scenario: Calls through the limit are allowed
- GIVEN a new session and agent pair
- WHEN exactly `MAX_CALLS` calls are checked
- THEN every call MUST be permitted
- AND the recorded count MUST equal `MAX_CALLS`

#### Scenario: Sessions and agents are isolated
- GIVEN calls are made by two agents in one session and one agent in another session
- WHEN their counts are inspected
- THEN each session-agent pair MUST have its own exact count

### Requirement: Reject the First Excess Call Actionably

The guard MUST raise `ToolLoopError` on call `MAX_CALLS + 1` and the error MUST identify the agent, session, observed count, and configured limit.

#### Scenario: First excess call is rejected
- GIVEN a session-agent pair has reached `MAX_CALLS`
- WHEN one additional call is checked
- THEN `ToolLoopError` MUST be raised
- AND the error MUST contain actionable session, agent, count, and limit details

#### Scenario: One exhausted key does not block another
- GIVEN one session-agent pair has exceeded its limit and another has not
- WHEN the second pair makes a call
- THEN the second pair MUST still be permitted

### Requirement: Reset Only the Requested Session

Resetting a session MUST remove counts for every agent in that session and MUST leave all other sessions unchanged.

#### Scenario: Existing session is reset
- GIVEN multiple agents have counts in one session and another session also has counts
- WHEN the first session is reset
- THEN all counts for the first session MUST be absent
- AND the other session's counts MUST be unchanged

#### Scenario: Unknown session is reset
- GIVEN a session identifier has no counts
- WHEN it is reset
- THEN the operation MUST complete without altering any existing session

### Requirement: Protect Shared State and Snapshot Ownership

Concurrent operations MUST preserve exact counts without lost updates, and each state snapshot MUST be an independent copy that callers cannot use to mutate guard state.

#### Scenario: Concurrent checks preserve count
- GIVEN multiple callers concurrently check the same session-agent pair without exceeding the limit
- WHEN all checks complete
- THEN the recorded count MUST equal the number of permitted checks

#### Scenario: Snapshot mutation is isolated
- GIVEN a caller obtains a state snapshot
- WHEN the caller mutates that snapshot
- THEN a later snapshot MUST reflect only actual guard operations
- AND external work MUST NOT be serialized as part of count ownership

---
