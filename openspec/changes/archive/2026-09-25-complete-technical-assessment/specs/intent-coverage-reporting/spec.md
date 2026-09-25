## Capability: intent-coverage-reporting

# Intent Coverage Reporting Specification

## Purpose

Define asynchronous, workspace-specific intent counts based on active catalog data and stored messages.

## Requirements

### Requirement: Reuse Supplied Shared Clients

The report MUST use the supplied database and storage singleton clients, MUST await their asynchronous operations, and MUST NOT instantiate replacement clients.

#### Scenario: Repeated reports reuse clients
- GIVEN the supplied singleton clients have each been initialized once
- WHEN reports are requested repeatedly
- THEN each client instantiation count MUST remain one

#### Scenario: Client operation fails
- GIVEN a supplied client raises an operational error other than the specified missing-workspace error
- WHEN a report is requested
- THEN the report MUST propagate the error
- AND MUST log workspace and operation context without credentials or message content

### Requirement: Initialize Active Intent Coverage

The report MUST include every active database intent initialized to zero, MUST always include `desconocido`, and MUST exclude inactive intents.

#### Scenario: Empty existing workspace
- GIVEN an existing workspace has no messages and the database has active and inactive intents
- WHEN its report is requested
- THEN every active intent and `desconocido` MUST have count zero
- AND no inactive intent MUST appear

#### Scenario: Mixed workspace messages
- GIVEN a workspace contains messages classified into multiple active intents and unknown
- WHEN its report is requested
- THEN each returned count MUST equal the exact number of matching workspace messages
- AND the sum of counts MUST equal the number of retrieved messages

### Requirement: Preserve Unsupported Results as Unknown

Any classifier result not present in the active database intent set MUST be counted as `desconocido` so that no message disappears from coverage totals.

#### Scenario: Classifier returns inactive intent
- GIVEN a workspace message classifies as an intent that exists but is inactive
- WHEN its report is requested
- THEN that message MUST increment `desconocido`
- AND the inactive intent MUST remain absent

#### Scenario: Classifier returns unregistered value
- GIVEN a workspace message classifies to a value absent from database intent records
- WHEN its report is requested
- THEN that message MUST increment `desconocido`

### Requirement: Distinguish Missing and Empty Workspaces

A missing workspace MUST propagate `KeyError`; a valid empty workspace MUST return the zero-initialized report; and report activity MUST produce useful non-sensitive logs.

#### Scenario: Missing workspace
- GIVEN the storage client identifies a workspace as nonexistent
- WHEN its report is requested
- THEN a `KeyError` MUST be propagated to the caller
- AND the event MUST be logged with the workspace identifier

#### Scenario: Successful report logging
- GIVEN an existing workspace
- WHEN its report completes
- THEN logs MUST identify the workspace and completion outcome
- AND logs MUST NOT disclose message bodies, credentials, or protected fixture contents

---
