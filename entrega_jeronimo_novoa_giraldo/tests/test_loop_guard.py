"""
Tests del EJERCICIO 5.

Aquí no te damos nada hecho a propósito: queremos ver qué casos se te ocurren.
Escribe la suite completa. Como mínimo debe cubrir:

  - se permiten hasta MAX_CALLS llamadas
  - la siguiente levanta ToolLoopError
  - el mensaje de error contiene agente, sesión y conteo
  - los conteos no se cruzan entre agentes
  - los conteos no se cruzan entre sesiones
  - reset() limpia una sesión y no afecta a las demás
  - snapshot() refleja los conteos actuales
"""

from concurrent.futures import ThreadPoolExecutor

import pytest

from tools.loop_guard import MAX_CALLS, LoopGuard, ToolLoopError


def test_calls_through_limit_are_allowed():
    guard = LoopGuard()

    counts = [guard.record("session-a", "classifier") for _ in range(MAX_CALLS)]

    assert counts == list(range(1, MAX_CALLS + 1))
    assert guard.snapshot("session-a") == {"classifier": MAX_CALLS}


def test_first_excess_call_is_actionable_and_does_not_advance_state():
    guard = LoopGuard()
    for _ in range(MAX_CALLS):
        guard.record("session-a", "classifier")

    with pytest.raises(ToolLoopError) as caught:
        guard.record("session-a", "classifier")

    message = str(caught.value)
    assert "session-a" in message
    assert "classifier" in message
    assert str(MAX_CALLS + 1) in message
    assert str(MAX_CALLS) in message
    assert guard.snapshot("session-a") == {"classifier": MAX_CALLS}


def test_agents_in_one_session_have_independent_counts():
    guard = LoopGuard()

    guard.record("session-a", "classifier")
    guard.record("session-a", "verifier")
    guard.record("session-a", "verifier")

    assert guard.snapshot("session-a") == {"classifier": 1, "verifier": 2}


def test_identical_agent_names_in_different_sessions_are_isolated():
    guard = LoopGuard()

    guard.record("session-a", "classifier")
    guard.record("session-b", "classifier")
    guard.record("session-b", "classifier")

    assert guard.snapshot("session-a") == {"classifier": 1}
    assert guard.snapshot("session-b") == {"classifier": 2}


def test_reset_removes_only_requested_session_and_unknown_is_noop():
    guard = LoopGuard()
    guard.record("session-a", "classifier")
    guard.record("session-a", "verifier")
    guard.record("session-b", "classifier")

    guard.reset("session-a")
    guard.reset("unknown-session")

    assert guard.snapshot("session-a") == {}
    assert guard.snapshot("session-b") == {"classifier": 1}


def test_snapshot_mutation_cannot_change_guard_state():
    guard = LoopGuard()
    guard.record("session-a", "classifier")

    snapshot = guard.snapshot("session-a")
    snapshot["classifier"] = 99
    snapshot["injected"] = 1

    assert guard.snapshot("session-a") == {"classifier": 1}


def test_concurrent_calls_for_one_key_lose_no_increments():
    call_count = 1_000
    guard = LoopGuard(max_calls=call_count)

    with ThreadPoolExecutor(max_workers=16) as executor:
        results = list(
            executor.map(
                lambda _: guard.record("session-a", "classifier"),
                range(call_count),
            )
        )

    assert sorted(results) == list(range(1, call_count + 1))
    assert guard.snapshot("session-a") == {"classifier": call_count}
