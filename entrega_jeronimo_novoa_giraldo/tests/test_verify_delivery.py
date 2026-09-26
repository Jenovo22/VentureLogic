import hashlib
import io
import json
from pathlib import Path

from tools.verify_delivery import (
    EXIT_INTEGRITY,
    EXIT_LEDGER,
    EXIT_OK,
    EXPECTED_DEPENDENCIES,
    _canonical_intents_hash,
    run_delivery_verification,
)


PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROTECTED_PATHS = (
    "fixtures/db.json",
    "fixtures/storage.json",
    "pytest.ini",
    "requirements.txt",
    "shared/clients.py",
    "shared/retriever.py",
    "tests/test_classify_intent.py",
)


def build_delivery_tree(tmp_path):
    for relative_path in PROTECTED_PATHS + ("config/intents.py",):
        source = PROJECT_ROOT / relative_path
        target = tmp_path / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(source.read_bytes())

    baseline = {
        "schema_version": 1,
        "hash_algorithm": "sha256",
        "files": {
            path: hashlib.sha256((tmp_path / path).read_bytes()).hexdigest()
            for path in PROTECTED_PATHS
        },
        "intents": {
            "sha256": _canonical_intents_hash(tmp_path / "config/intents.py")
        },
    }
    baseline_path = tmp_path / "evidence/protected_baseline.json"
    baseline_path.parent.mkdir(parents=True)
    baseline_path.write_text(json.dumps(baseline), encoding="utf-8")
    return baseline_path, tmp_path / "evidence/pending_source_corrections.jsonl"


def run_verifier(tmp_path):
    baseline_path, ledger_path = build_delivery_tree(tmp_path)
    output = io.StringIO()
    exit_code = run_delivery_verification(
        tmp_path, baseline_path, ledger_path, output
    )
    return exit_code, output.getvalue(), ledger_path


def test_verifier_accepts_matching_delivery_and_empty_ledger(tmp_path):
    exit_code, output, _ = run_verifier(tmp_path)

    assert exit_code == EXIT_OK
    assert "PASS protected files: 7 SHA-256 values match" in output
    assert "PASS canonical INTENTS hash" in output
    assert "PASS dependency declaration and set unchanged" in output
    assert output.endswith("0 unresolved pending corrections\n")


def test_verifier_rejects_protected_file_mismatch(tmp_path):
    baseline_path, ledger_path = build_delivery_tree(tmp_path)
    (tmp_path / "shared/clients.py").write_text("changed", encoding="utf-8")
    output = io.StringIO()

    exit_code = run_delivery_verification(
        tmp_path, baseline_path, ledger_path, output
    )

    assert exit_code == EXIT_INTEGRITY
    assert "ERROR integrity: shared/clients.py: SHA-256 mismatch" in output.getvalue()


def test_verifier_rejects_malformed_ledger(tmp_path):
    baseline_path, ledger_path = build_delivery_tree(tmp_path)
    ledger_path.write_text("{not-json}\n", encoding="utf-8")
    output = io.StringIO()

    exit_code = run_delivery_verification(
        tmp_path, baseline_path, ledger_path, output
    )

    assert exit_code == EXIT_LEDGER
    assert "ERROR pending correction ledger: Malformed correction ledger at line 1" in output.getvalue()


def test_verifier_reports_valid_pending_record_without_failure(tmp_path):
    baseline_path, ledger_path = build_delivery_tree(tmp_path)
    record = {
        "schema_version": 1,
        "status": "pending",
        "workspace_id": "acme",
        "answer_id": "a-4",
        "source_id": "src-missing",
        "reason": "missing_source",
        "detail": "Referenced source was not found.",
        "first_observed_at": "2026-09-25T12:00:00Z",
    }
    ledger_path.write_text(json.dumps(record) + "\n", encoding="utf-8")
    output = io.StringIO()

    exit_code = run_delivery_verification(
        tmp_path, baseline_path, ledger_path, output
    )

    assert exit_code == EXIT_OK
    assert "unresolved pending correction:" in output.getvalue()
    assert '"answer_id": "a-4"' in output.getvalue()
    assert '"source_id": "src-missing"' in output.getvalue()
    assert EXPECTED_DEPENDENCIES == frozenset(
        {"pytest>=8.0", "pytest-asyncio>=0.23"}
    )
