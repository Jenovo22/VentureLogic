"""
Tests del EJERCICIO 6.

Te damos DOS: el camino feliz y el camino de abstención, que es el que de
verdad importa. Agrega al menos DOS más — el caso `DUDOSO` y algún borde
(pregunta vacía, workspace inexistente, pregunta sin ninguna palabra en común
con el corpus).

Fíjate que estos tests no levantan el servidor: llaman a `consultar()`
directamente. Si tu lógica quedó atrapada dentro del handler HTTP, no vas a
poder escribirlos, y eso ya es una señal sobre el diseño.
"""

import re

import pytest

import app
from app import UMBRAL_MINIMO, consultar


@pytest.mark.asyncio
async def test_pregunta_sustentada_devuelve_respuesta_con_fuente():
    r = await consultar("¿Cuántos días de garantía tiene el plan Pro?", "acme")

    assert r["veredicto"] == "APROBADO"
    assert r["respuesta"] is not None
    assert "15 días" in r["respuesta"]
    assert r["fragmentos"][0]["source_id"] == "src-1"
    assert r["fragmentos"][0]["similitud"] >= UMBRAL_MINIMO


@pytest.mark.asyncio
async def test_pregunta_sin_evidencia_no_inventa_respuesta():
    # El corpus no dice nada del plan Enterprise. El recuperador igual devuelve
    # fragmentos parecidos —habla de planes y de garantías— pero ninguno responde.
    r = await consultar("¿cuánto dura la garantía del plan Enterprise?", "acme")

    assert r["veredicto"] == "SIN_EVIDENCIA"
    assert r["respuesta"] is None
    assert r["fragmentos"], "el recuperador sí devolvió fragmentos"
    assert r["fragmentos"][0]["similitud"] < UMBRAL_MINIMO
    assert "0.55" in r["motivo"] or "55" in r["motivo"], "el motivo debe citar el umbral"


EXPECTED_KEYS = {
    "pregunta",
    "workspace",
    "intencion",
    "especialista",
    "fragmentos",
    "veredicto",
    "motivo",
    "respuesta",
}


@pytest.mark.asyncio
async def test_conserva_todos_los_fragmentos_y_elige_el_maximo_real(monkeypatch):
    fragmentos = [
        {
            "source_id": "src-bajo",
            "titulo": "Bajo",
            "chunk": 0,
            "texto": "Texto con evidencia menor.",
            "similitud": 0.56,
        },
        {
            "source_id": "src-alto",
            "titulo": "Alto",
            "chunk": 2,
            "texto": "Texto exacto de la evidencia superior.",
            "similitud": 0.91,
        },
        {
            "source_id": "src-medio",
            "titulo": "Medio",
            "chunk": 1,
            "texto": "Texto con evidencia intermedia.",
            "similitud": 0.74,
        },
    ]

    async def search_unsorted(_pregunta):
        return fragmentos

    monkeypatch.setattr(app, "search", search_unsorted)

    resultado = await consultar("Necesito información de pago", "globex")

    assert set(resultado) == EXPECTED_KEYS
    assert resultado["pregunta"] == "Necesito información de pago"
    assert resultado["workspace"] == "globex"
    assert resultado["intencion"] == "facturacion"
    assert resultado["especialista"] == "billing_agent"
    assert resultado["fragmentos"] == fragmentos
    assert resultado["fragmentos"] is not fragmentos
    assert all(copia is not original for copia, original in zip(resultado["fragmentos"], fragmentos))
    assert resultado["veredicto"] == "APROBADO"
    assert "0.91" in resultado["motivo"]
    assert "0.75" in resultado["motivo"]
    assert resultado["respuesta"] == "Texto exacto de la evidencia superior."


@pytest.mark.asyncio
@pytest.mark.parametrize("pregunta", ["", "xyzzy plugh"])
async def test_sin_fragmentos_o_sin_solapamiento_se_abstiene(pregunta):
    resultado = await consultar(pregunta, "acme")

    assert set(resultado) == EXPECTED_KEYS
    assert resultado["fragmentos"] == []
    assert resultado["veredicto"] == "SIN_EVIDENCIA"
    assert resultado["respuesta"] is None
    assert "fragmentos" in resultado["motivo"].lower()
    assert "0.55" in resultado["motivo"]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("similitud", "veredicto", "responde"),
    [
        (0.549999, "SIN_EVIDENCIA", False),
        (0.55, "DUDOSO", True),
        (0.749999, "DUDOSO", True),
        (0.75, "APROBADO", True),
    ],
)
async def test_aplica_los_limites_exactos(monkeypatch, similitud, veredicto, responde):
    texto = f"Evidencia exacta para {similitud}."

    async def search_at_boundary(_pregunta):
        return [{
            "source_id": "src-limite",
            "titulo": "Límites",
            "chunk": 0,
            "texto": texto,
            "similitud": similitud,
        }]

    monkeypatch.setattr(app, "search", search_at_boundary)

    resultado = await consultar("Consulta sin intención conocida", "initech")

    assert resultado["veredicto"] == veredicto
    assert str(similitud) in resultado["motivo"]
    assert "0.55" in resultado["motivo"]
    assert "0.75" in resultado["motivo"]
    assert resultado["respuesta"] == (texto if responde else None)


def test_safe_render_pagina_usa_solo_sumideros_de_texto():
    pagina = app.PAGINA
    script = re.search(r"<script>(.*?)</script>", pagina, re.DOTALL).group(1)

    assert "document.createElement" in script
    assert ".textContent" in script
    assert "innerHTML" not in pagina
    assert not re.search(r"`[^`]*\$\{data(?:\.|\[)", script)

    for campo in (
        "pregunta", "workspace", "intencion", "especialista", "fragmentos",
        "source_id", "titulo", "chunk", "texto", "similitud", "veredicto",
        "motivo", "respuesta",
    ):
        assert campo in script


def test_safe_render_pagina_codifica_pregunta_y_workspace():
    assert "encodeURIComponent(q)" in app.PAGINA
    assert "encodeURIComponent(ws)" in app.PAGINA


def test_safe_render_pagina_expone_pipeline_fragmentos_y_abstencion():
    pagina = app.PAGINA

    for etiqueta in ("Intención", "Especialista", "Fragmentos recuperados", "Motivo", "Respuesta"):
        assert etiqueta in pagina
    for veredicto in ("APROBADO", "DUDOSO", "SIN_EVIDENCIA"):
        assert veredicto in pagina
        assert f"verdict-{veredicto}" in pagina

    assert "Fragmento seleccionado" in pagina
    assert "No hay evidencia suficiente para responder." in pagina
    assert "setAttribute('role', 'status')" in pagina
