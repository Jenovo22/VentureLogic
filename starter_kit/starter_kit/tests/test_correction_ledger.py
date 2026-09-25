"""Focused tests for the durable pending-correction ledger."""

import json
from concurrent.futures import ThreadPoolExecutor

import pytest

from tools.correction_ledger import CorrectionLedgerError, PendingCorrectionLedger


def test_ledger_handles_missing_and_empty_files(tmp_path):
    path = tmp_path / "nested" / "pending.jsonl"
    ledger = PendingCorrectionLedger(path)

    assert ledger.pending() == []
    path.parent.mkdir(parents=True)
    path.write_text("", encoding="utf-8")
    assert ledger.pending() == []


def test_ledger_rejects_malformed_jsonl_explicitly(tmp_path):
    path = tmp_path / "pending.jsonl"
    path.write_text("not-json\n", encoding="utf-8")

    with pytest.raises(CorrectionLedgerError, match="line 1"):
        PendingCorrectionLedger(path).pending()


def test_ledger_deduplicates_concurrent_records_and_remains_parseable(tmp_path):
    path = tmp_path / "pending.jsonl"
    ledger = PendingCorrectionLedger(path)
    correction = {
        "workspace_id": "alpha",
        "answer_id": "a-1",
        "source_id": "missing",
        "reason": "missing_source",
        "detail": "Referenced source was not found.",
    }

    with ThreadPoolExecutor(max_workers=8) as executor:
        list(executor.map(ledger.record, [correction] * 40))

    records = ledger.pending()
    assert len(records) == 1
    assert records[0] == {
        "schema_version": 1,
        "status": "pending",
        **correction,
        "first_observed_at": records[0]["first_observed_at"],
    }
    assert records[0]["first_observed_at"].endswith("Z")
    assert json.loads(path.read_text(encoding="utf-8").strip()) == records[0]
