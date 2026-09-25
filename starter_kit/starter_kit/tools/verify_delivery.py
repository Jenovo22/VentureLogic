"""Verify immutable delivery inputs and report pending source corrections."""

from __future__ import annotations

import ast
import hashlib
import json
import sys
from pathlib import Path
from typing import TextIO

from tools.correction_ledger import CorrectionLedgerError, PendingCorrectionLedger


PROJECT_ROOT = Path(__file__).resolve().parent.parent
BASELINE_PATH = PROJECT_ROOT / "evidence" / "protected_baseline.json"
LEDGER_PATH = PROJECT_ROOT / "evidence" / "pending_source_corrections.jsonl"
EXPECTED_DEPENDENCIES = frozenset({"pytest>=8.0", "pytest-asyncio>=0.23"})

EXIT_OK = 0
EXIT_INTEGRITY = 1
EXIT_BASELINE = 2
EXIT_LEDGER = 3


class BaselineError(ValueError):
    """Raised when the protected baseline cannot be trusted."""


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _load_baseline(path: Path) -> dict:
    try:
        baseline = json.loads(path.read_text(encoding="utf-8"))
        files = baseline["files"]
        intents_hash = baseline["intents"]["sha256"]
    except (OSError, UnicodeError, json.JSONDecodeError, KeyError, TypeError) as error:
        raise BaselineError(f"cannot load protected baseline: {error}") from error

    if (
        baseline.get("schema_version") != 1
        or baseline.get("hash_algorithm") != "sha256"
        or not isinstance(files, dict)
        or not files
        or not all(isinstance(key, str) and isinstance(value, str) for key, value in files.items())
        or not isinstance(intents_hash, str)
    ):
        raise BaselineError("protected baseline schema is invalid")
    return baseline


def _canonical_intents_hash(path: Path) -> str:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in tree.body:
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            if any(isinstance(target, ast.Name) and target.id == "INTENTS" for target in targets):
                literal = ast.literal_eval(node.value)
                canonical = json.dumps(
                    literal,
                    ensure_ascii=False,
                    sort_keys=True,
                    separators=(",", ":"),
                ).encode("utf-8")
                return _sha256(canonical)
    raise BaselineError("INTENTS AST literal was not found")


def _dependency_set(path: Path) -> frozenset[str]:
    declarations = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        declaration = line.split("#", 1)[0].strip()
        if declaration:
            declarations.add(declaration)
    return frozenset(declarations)


def run_delivery_verification(
    root: Path = PROJECT_ROOT,
    baseline_path: Path = BASELINE_PATH,
    ledger_path: Path = LEDGER_PATH,
    stream: TextIO = sys.stdout,
) -> int:
    """Run read-only delivery checks and return a documented process exit code."""
    integrity_errors: list[str] = []
    baseline_error: str | None = None

    try:
        baseline = _load_baseline(baseline_path)
        for relative_path, expected_hash in sorted(baseline["files"].items()):
            protected_path = root / relative_path
            try:
                actual_hash = _sha256(protected_path.read_bytes())
            except OSError as error:
                integrity_errors.append(f"{relative_path}: cannot read file: {error}")
                continue
            if actual_hash != expected_hash:
                integrity_errors.append(
                    f"{relative_path}: SHA-256 mismatch; expected {expected_hash}, got {actual_hash}"
                )

        intents_hash = _canonical_intents_hash(root / "config" / "intents.py")
        expected_intents_hash = baseline["intents"]["sha256"]
        if intents_hash != expected_intents_hash:
            integrity_errors.append(
                "INTENTS: canonical hash mismatch; "
                f"expected {expected_intents_hash}, got {intents_hash}"
            )

        dependencies = _dependency_set(root / "requirements.txt")
        added_dependencies = sorted(dependencies - EXPECTED_DEPENDENCIES)
        if added_dependencies:
            integrity_errors.append(
                "requirements.txt: dependency set expanded with "
                + ", ".join(added_dependencies)
            )
    except (BaselineError, OSError, UnicodeError, SyntaxError, ValueError) as error:
        baseline_error = str(error)

    ledger_error: str | None = None
    pending: list[dict] = []
    try:
        pending = PendingCorrectionLedger(ledger_path).pending()
    except (CorrectionLedgerError, OSError, UnicodeError) as error:
        ledger_error = str(error)

    if baseline_error:
        print(f"ERROR baseline: {baseline_error}", file=stream)
    elif integrity_errors:
        for error in integrity_errors:
            print(f"ERROR integrity: {error}", file=stream)
    else:
        print(f"PASS protected files: {len(baseline['files'])} SHA-256 values match", file=stream)
        print("PASS canonical INTENTS hash", file=stream)
        print("PASS dependency declaration and set unchanged", file=stream)

    if ledger_error:
        print(f"ERROR pending correction ledger: {ledger_error}", file=stream)
    elif not pending:
        print("0 unresolved pending corrections", file=stream)
    else:
        for record in pending:
            print(
                "unresolved pending correction: "
                + json.dumps(record, ensure_ascii=False, sort_keys=True),
                file=stream,
            )

    if baseline_error:
        return EXIT_BASELINE
    if ledger_error:
        return EXIT_LEDGER
    if integrity_errors:
        return EXIT_INTEGRITY
    return EXIT_OK


def main() -> int:
    return run_delivery_verification()


if __name__ == "__main__":
    raise SystemExit(main())
