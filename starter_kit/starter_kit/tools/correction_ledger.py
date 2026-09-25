"""Durable audit ledger for legacy answers omitted due to invalid sources."""

from __future__ import annotations

import json
import os
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Mapping


DEFAULT_LEDGER_PATH = (
    Path(__file__).resolve().parent.parent
    / "evidence"
    / "pending_source_corrections.jsonl"
)
REASONS = {"missing_source", "malformed_source", "missing_title"}
REQUIRED_FIELDS = {
    "schema_version",
    "status",
    "workspace_id",
    "answer_id",
    "source_id",
    "reason",
    "detail",
    "first_observed_at",
}


class CorrectionLedgerError(ValueError):
    """Raised when a persisted correction ledger cannot be trusted."""


class PendingCorrectionLedger:
    """Append-only, thread-safe pending-correction ledger with stable dedupe."""

    def __init__(self, path: Path = DEFAULT_LEDGER_PATH) -> None:
        self.path = Path(path)
        self._lock = threading.Lock()

    def pending(self) -> list[dict]:
        """Return parsed pending records, rejecting malformed persisted state."""
        with self._lock:
            return self._read_records()

    def record(self, correction: Mapping[str, object]) -> None:
        """Persist one unique pending defect without attempting remediation."""
        record = self._build_record(correction)
        stable_key = self._stable_key(record)

        with self._lock:
            records = self._read_records()
            if any(self._stable_key(item) == stable_key for item in records):
                return

            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.open("a", encoding="utf-8") as ledger_file:
                json.dump(record, ledger_file, ensure_ascii=False, sort_keys=True)
                ledger_file.write("\n")
                ledger_file.flush()
                os.fsync(ledger_file.fileno())

    def _read_records(self) -> list[dict]:
        if not self.path.exists() or self.path.stat().st_size == 0:
            return []

        records = []
        with self.path.open(encoding="utf-8") as ledger_file:
            for line_number, line in enumerate(ledger_file, start=1):
                if not line.strip():
                    continue
                try:
                    record = json.loads(line)
                    self._validate_persisted(record)
                except (json.JSONDecodeError, CorrectionLedgerError) as error:
                    raise CorrectionLedgerError(
                        f"Malformed correction ledger at line {line_number}: {error}"
                    ) from error
                records.append(record)
        return records

    @staticmethod
    def _build_record(correction: Mapping[str, object]) -> dict:
        reason = correction.get("reason")
        if reason not in REASONS:
            raise CorrectionLedgerError(f"Unsupported correction reason: {reason!r}")

        return {
            "schema_version": 1,
            "status": "pending",
            "workspace_id": str(correction.get("workspace_id", "")),
            "answer_id": str(correction.get("answer_id", "")),
            "source_id": correction.get("source_id"),
            "reason": reason,
            "detail": str(correction.get("detail", "")),
            "first_observed_at": datetime.now(timezone.utc)
            .isoformat()
            .replace("+00:00", "Z"),
        }

    @staticmethod
    def _validate_persisted(record: object) -> None:
        if not isinstance(record, dict):
            raise CorrectionLedgerError("record is not a JSON object")
        if set(record) != REQUIRED_FIELDS:
            raise CorrectionLedgerError("record fields do not match schema version 1")
        if record["schema_version"] != 1 or record["status"] != "pending":
            raise CorrectionLedgerError("unsupported schema version or status")
        if record["reason"] not in REASONS:
            raise CorrectionLedgerError("unsupported correction reason")

    @staticmethod
    def _stable_key(record: Mapping[str, object]) -> tuple[object, ...]:
        return (
            record["workspace_id"],
            record["answer_id"],
            record["source_id"],
            record["reason"],
        )


DEFAULT_LEDGER = PendingCorrectionLedger()
