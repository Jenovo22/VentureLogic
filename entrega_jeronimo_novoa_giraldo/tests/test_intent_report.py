"""
Tests del EJERCICIO 2.

Te damos UN test de ejemplo para que veas el estilo. Debes agregar al menos
CUATRO más, cubriendo:

  - un workspace con mensajes variados (verifica los conteos exactos)
  - un workspace vacío
  - la intención inactiva de la base de datos (`ventas`) — no debe aparecer
  - un workspace inexistente — el comportamiento que tú decidiste y documentaste
  - que NO se instancian clientes nuevos (usa `clients._INSTANTIATIONS`)

Nombra cada test de forma que al leer el nombre se entienda qué protege.
"""

import pytest

from shared import clients
from tools import intent_report_tool
from tools.intent_report_tool import count_messages_by_intent


@pytest.mark.asyncio
async def test_globex_solo_tiene_mensajes_de_soporte():
    result = await count_messages_by_intent("globex")

    assert result["soporte_tecnico"] == 4
    assert result["facturacion"] == 0
    assert result["cuenta"] == 0
    assert result["desconocido"] == 0


@pytest.mark.asyncio
async def test_acme_cuenta_todos_los_mensajes_en_intenciones_activas(caplog):
    caplog.set_level("INFO")
    result = await count_messages_by_intent("acme")

    assert result == {
        "facturacion": 3,
        "soporte_tecnico": 1,
        "cuenta": 3,
        "desconocido": 3,
    }
    assert sum(result.values()) == 10
    assert "acme" in caplog.text
    assert "completado" in caplog.text
    assert "Me llegó una factura duplicada este mes" not in caplog.text


@pytest.mark.asyncio
async def test_workspace_vacio_incluye_intenciones_activas_en_cero():
    result = await count_messages_by_intent("initech")

    assert result == {
        "facturacion": 0,
        "soporte_tecnico": 0,
        "cuenta": 0,
        "desconocido": 0,
    }
    assert "ventas" not in result


@pytest.mark.asyncio
async def test_resultados_inactivos_o_no_registrados_cuentan_como_desconocidos(
    monkeypatch,
):
    storage = clients.get_storage_client()
    storage._data["unsupported"] = ["inactive", "unregistered"]
    classifications = iter(["ventas", "intencion_no_registrada"])
    monkeypatch.setattr(
        intent_report_tool,
        "classify_intent",
        lambda _message: next(classifications),
    )

    result = await count_messages_by_intent("unsupported")

    assert result["desconocido"] == 2
    assert sum(result.values()) == 2
    assert "ventas" not in result
    assert "intencion_no_registrada" not in result


@pytest.mark.asyncio
async def test_workspace_inexistente_propaga_key_error_y_registra_contexto(caplog):
    with pytest.raises(KeyError, match="missing"):
        await count_messages_by_intent("missing")

    assert "missing" in caplog.text
    assert "list_messages" in caplog.text


@pytest.mark.asyncio
@pytest.mark.parametrize("failing_operation", ["intents.get", "list_messages"])
async def test_error_operacional_se_propaga_sin_exponer_datos_sensibles(
    caplog,
    monkeypatch,
    failing_operation,
):
    secret = "credential=super-secret"

    class FailingTable:
        async def get(self):
            raise RuntimeError(secret)

    class FailingDatabase:
        def table(self, _name):
            return FailingTable()

    class FailingStorage:
        async def list_messages(self, _workspace_id):
            raise RuntimeError(secret)

    if failing_operation == "intents.get":
        monkeypatch.setattr(
            intent_report_tool,
            "get_db_client",
            lambda: FailingDatabase(),
        )
    else:
        monkeypatch.setattr(
            intent_report_tool,
            "get_storage_client",
            lambda: FailingStorage(),
        )

    with pytest.raises(RuntimeError, match="super-secret"):
        await count_messages_by_intent("acme")

    assert "acme" in caplog.text
    assert failing_operation in caplog.text
    assert secret not in caplog.text


@pytest.mark.asyncio
async def test_llamadas_repetidas_reutilizan_los_singletons():
    await count_messages_by_intent("acme")
    await count_messages_by_intent("globex")

    assert clients._INSTANTIATIONS == {"db": 1, "storage": 1}
