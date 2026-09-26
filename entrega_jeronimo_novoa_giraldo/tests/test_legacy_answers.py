"""Regression tests for isolated legacy-answer retrieval and omission auditing."""

from __future__ import annotations

import asyncio
from pathlib import Path

import pytest

from shared import clients
from shared.clients import Record
from tools import legacy_answers_tool


class RecordingLedger:
    def __init__(self):
        self.corrections = []

    def record(self, correction):
        self.corrections.append(correction)


class FakeTable:
    def __init__(self, name, rows, counters):
        self.name = name
        self.rows = rows
        self.counters = counters
        self.workspace_id = None

    def where(self, _field, value):
        self.workspace_id = value
        return self

    async def get(self):
        self.counters[self.name] = self.counters.get(self.name, 0) + 1
        rows = self.rows
        if self.name == "answers":
            rows = {
                key: value
                for key, value in rows.items()
                if value.get("workspace_id") == self.workspace_id
            }
        return [Record(record_id, value) for record_id, value in rows.items()]

    def item(self, record_id):
        self.counters["source_items"] = self.counters.get("source_items", 0) + 1

        class Item:
            async def get(inner_self):
                return Record(record_id, self.rows.get(record_id))

        return Item()


class FakeDatabase:
    def __init__(self, answers, sources):
        self.answers = answers
        self.sources = sources
        self.counters = {}

    def table(self, name):
        rows = self.answers if name == "answers" else self.sources
        return FakeTable(name, rows, self.counters)


def install_database(monkeypatch, database):
    monkeypatch.setattr(
        legacy_answers_tool,
        "get_db_client",
        lambda: database,
        raising=False,
    )
    monkeypatch.setattr(
        legacy_answers_tool,
        "DatabaseClient",
        lambda: database,
        raising=False,
    )


async def retrieve(workspace_id, *, threshold=0.0, ledger=None):
    kwargs = {"min_similitud": threshold}
    if ledger is not None:
        kwargs["ledger"] = ledger
    try:
        return await legacy_answers_tool.get_workspace_answers(workspace_id, **kwargs)
    except TypeError as error:
        if "ledger" not in str(error):
            raise
        kwargs.pop("ledger")
        return await legacy_answers_tool.get_workspace_answers(workspace_id, **kwargs)


@pytest.fixture
def answer_data():
    return {
        "a-1": {
            "workspace_id": "alpha",
            "source_id": "src-1",
            "respuesta": "Alpha",
            "similitud": 0.55,
        },
        "a-2": {
            "workspace_id": "alpha",
            "source_id": "src-2",
            "respuesta": "High",
            "similitud": 0.90,
        },
        "b-1": {
            "workspace_id": "beta",
            "source_id": "src-2",
            "respuesta": "Beta",
            "similitud": 0.75,
        },
    }


@pytest.fixture
def source_data():
    return {
        "src-1": {"titulo": "Source one"},
        "src-2": {"titulo": "Source two"},
    }


@pytest.mark.asyncio
async def test_consecutive_workspaces_and_thresholds_are_isolated(
    monkeypatch, answer_data, source_data
):
    database = FakeDatabase(answer_data, source_data)
    install_database(monkeypatch, database)
    ledger = RecordingLedger()

    alpha = await retrieve("alpha", threshold=0.0, ledger=ledger)
    beta = await retrieve("beta", threshold=0.0, ledger=ledger)
    strict_alpha = await retrieve("alpha", threshold=0.80, ledger=ledger)

    assert [item["respuesta"] for item in alpha] == ["Alpha", "High"]
    assert [item["respuesta"] for item in beta] == ["Beta"]
    assert [item["respuesta"] for item in strict_alpha] == ["High"]


@pytest.mark.asyncio
async def test_returned_results_have_fresh_ownership(monkeypatch, answer_data, source_data):
    database = FakeDatabase(answer_data, source_data)
    install_database(monkeypatch, database)
    ledger = RecordingLedger()

    first = await retrieve("alpha", ledger=ledger)
    first[0]["respuesta"] = "caller mutation"
    first.append({"unexpected": True})
    second = await retrieve("alpha", ledger=ledger)

    assert [item["respuesta"] for item in second] == ["Alpha", "High"]
    assert first is not second
    assert first[0] is not second[0]


@pytest.mark.asyncio
async def test_threshold_is_inclusive_and_sources_are_fetched_once(
    monkeypatch, answer_data, source_data
):
    database = FakeDatabase(answer_data, source_data)
    install_database(monkeypatch, database)

    result = await retrieve("alpha", threshold=0.55, ledger=RecordingLedger())

    assert [item["respuesta"] for item in result] == ["Alpha", "High"]
    assert database.counters == {"answers": 1, "sources": 1}


@pytest.mark.asyncio
async def test_no_eligible_answers_returns_fresh_empty_without_source_read(
    monkeypatch, answer_data, source_data
):
    database = FakeDatabase(answer_data, source_data)
    install_database(monkeypatch, database)

    first = await retrieve("alpha", threshold=1.0, ledger=RecordingLedger())
    second = await retrieve("alpha", threshold=1.0, ledger=RecordingLedger())

    assert first == []
    assert second == []
    assert first is not second
    assert database.counters == {"answers": 2}


@pytest.mark.asyncio
async def test_reuses_database_singleton_across_requests():
    ledger = RecordingLedger()

    await retrieve("globex", ledger=ledger)
    await retrieve("initech", ledger=ledger)

    assert clients._INSTANTIATIONS["db"] == 1


@pytest.mark.asyncio
async def test_does_not_create_real_or_shared_temp_output(
    monkeypatch, answer_data, source_data
):
    answer_data["g-1"] = {
        "workspace_id": "gamma",
        "source_id": "src-1",
        "respuesta": "Gamma",
        "similitud": 0.80,
    }
    database = FakeDatabase(answer_data, source_data)
    install_database(monkeypatch, database)
    intercepted_paths = []

    def intercept_write(path, *_args, **_kwargs):
        intercepted_paths.append(str(path))

    monkeypatch.setattr(
        Path,
        "write_text",
        intercept_write,
    )

    await retrieve("gamma", ledger=RecordingLedger())

    assert intercepted_paths == []


@pytest.mark.asyncio
async def test_invalid_sources_are_logged_recorded_and_omitted(
    caplog, monkeypatch
):
    answers = {
        "valid": {
            "workspace_id": "alpha",
            "source_id": "src-valid",
            "respuesta": "Keep me",
            "similitud": 0.90,
        },
        "missing": {
            "workspace_id": "alpha",
            "source_id": "src-absent",
            "respuesta": "Omit missing",
            "similitud": 0.90,
        },
        "malformed": {
            "workspace_id": "alpha",
            "source_id": "src-malformed",
            "respuesta": "Omit malformed",
            "similitud": 0.90,
        },
        "titleless": {
            "workspace_id": "alpha",
            "source_id": "src-titleless",
            "respuesta": "Omit titleless",
            "similitud": 0.90,
        },
    }
    database = FakeDatabase(
        answers,
        {
            "src-valid": {"titulo": "Valid title"},
            "src-malformed": "not-a-record",
            "src-titleless": {"texto": "No title"},
        },
    )
    install_database(monkeypatch, database)
    ledger = RecordingLedger()
    caplog.set_level("WARNING")

    result = await retrieve("alpha", ledger=ledger)

    assert result == [
        {
            **answers["valid"],
            "fuente_titulo": "Valid title",
            "confianza": "alta",
        }
    ]
    assert "source_status" not in result[0]
    assert {(item["answer_id"], item["source_id"], item["reason"]) for item in ledger.corrections} == {
        ("missing", "src-absent", "missing_source"),
        ("malformed", "src-malformed", "malformed_source"),
        ("titleless", "src-titleless", "missing_title"),
    }
    for identifier in ("missing", "malformed", "titleless"):
        assert identifier in caplog.text
    for reason in ("missing_source", "malformed_source", "missing_title"):
        assert reason in caplog.text


@pytest.mark.asyncio
async def test_concurrent_retrievals_do_not_share_mutable_results(
    monkeypatch, answer_data, source_data
):
    database = FakeDatabase(answer_data, source_data)
    install_database(monkeypatch, database)
    alpha, beta = await asyncio.gather(
        retrieve("alpha", ledger=RecordingLedger()),
        retrieve("beta", ledger=RecordingLedger()),
    )

    assert [item["workspace_id"] for item in alpha] == ["alpha", "alpha"]
    assert [item["workspace_id"] for item in beta] == ["beta"]
