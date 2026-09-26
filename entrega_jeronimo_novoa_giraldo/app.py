"""
Consola del Asistente — EJERCICIO 6.

Arranca así:

    python app.py            # http://localhost:8000

El servidor, el pipeline y la página están implementados. Al ejecutarlo puedes
consultar la evidencia local y ver la intención, los fragmentos, el veredicto y
la respuesta o abstención resultante.

NO agregues dependencias. Todo esto sale de la librería estándar a propósito:
nada de Flask, FastAPI, React ni CSS externo. Feo pero claro está bien —
no evaluamos diseño gráfico, evaluamos que se entienda lo que pasó.
"""

from __future__ import annotations

import asyncio
import json
import logging
import re
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

from config.intents import classify_intent, specialist_for
from shared.retriever import search

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger("consola")

PUERTO = 8000

# Umbrales de decisión. Son un punto de partida, no una verdad revelada:
# si los cambias, di por qué en NOTAS.md.
UMBRAL_MINIMO = 0.55   # por debajo de esto no hay evidencia suficiente
UMBRAL_ALTO = 0.75     # por debajo de esto la respuesta va marcada como dudosa

_REESTABLECER_VARIANT = re.compile(r"\breestabl(?=e(?:c|z))", re.IGNORECASE)


def _normalize_retrieval_query(pregunta: str) -> str:
    """Normaliza una variante ortográfica solo para recuperar evidencia."""
    return _REESTABLECER_VARIANT.sub("restabl", pregunta)


# ---------------------------------------------------------------------------
# PIPELINE DE CONSULTA
# ---------------------------------------------------------------------------

async def consultar(pregunta: str, workspace_id: str = "acme") -> dict:
    """Ejecuta el pipeline completo sobre una pregunta y devuelve qué pasó.

    Esta función es el corazón del ejercicio y debe ser **testeable sin
    levantar el servidor**: recibe texto, devuelve un diccionario.

    Pasos:

    1. **Clasificar** la intención con `config.intents.classify_intent`.
    2. **Recuperar** fragmentos con `shared.retriever.search`.
    3. **Decidir** el veredicto según el mejor puntaje de similitud:
       - `SIN_EVIDENCIA` si no hay fragmentos o el mejor queda por debajo de
         `UMBRAL_MINIMO`. En este caso **no se responde**: `respuesta` es
         `None`. Este camino es el más importante de los tres.
       - `DUDOSO` si el mejor está entre `UMBRAL_MINIMO` y `UMBRAL_ALTO`.
         Se responde, pero marcado para revisión.
       - `APROBADO` si el mejor llega a `UMBRAL_ALTO` o más.
    4. **Redactar**: en esta prueba no hay modelo de lenguaje ni llamadas a
       ninguna API. La "respuesta" es el texto literal del mejor fragmento.
       Así se garantiza que nada de lo que muestra la consola esté inventado.

    Devuelve exactamente esta forma (los tests y la página dependen de ella):

        {
          "pregunta":    "¿Cuántos días de garantía tiene el plan Pro?",
          "workspace":   "acme",
          "intencion":   "facturacion",
          "especialista": "billing_agent",     # o None si la intención es desconocida
          "fragmentos":  [ {source_id, titulo, chunk, texto, similitud}, ... ],
          "veredicto":   "APROBADO" | "DUDOSO" | "SIN_EVIDENCIA",
          "motivo":      "Similitud 0.37, por debajo del mínimo de 0.55",
          "respuesta":   "El plan Pro incluye…"   # None si SIN_EVIDENCIA
        }

    El `motivo` lo lee un humano cuando algo sale raro: que diga números.
    """
    intencion = classify_intent(pregunta)
    especialista = specialist_for(intencion)
    consulta_recuperacion = _normalize_retrieval_query(pregunta)
    fragmentos = [dict(fragmento) for fragmento in await search(consulta_recuperacion)]

    if not fragmentos:
        veredicto = "SIN_EVIDENCIA"
        motivo = (
            "No se recuperaron fragmentos; se requiere una similitud mínima "
            f"de {UMBRAL_MINIMO:g} para responder."
        )
        respuesta = None
    else:
        mejor_fragmento = max(fragmentos, key=lambda fragmento: fragmento["similitud"])
        similitud = mejor_fragmento["similitud"]

        if similitud < UMBRAL_MINIMO:
            veredicto = "SIN_EVIDENCIA"
            motivo = (
                f"Similitud máxima {similitud:g}, por debajo del mínimo de "
                f"{UMBRAL_MINIMO:g}; la aprobación requiere {UMBRAL_ALTO:g}."
            )
            respuesta = None
        elif similitud < UMBRAL_ALTO:
            veredicto = "DUDOSO"
            motivo = (
                f"Similitud máxima {similitud:g}, desde el mínimo de "
                f"{UMBRAL_MINIMO:g} pero por debajo de {UMBRAL_ALTO:g}."
            )
            respuesta = mejor_fragmento["texto"]
        else:
            veredicto = "APROBADO"
            motivo = (
                f"Similitud máxima {similitud:g}, igual o superior a "
                f"{UMBRAL_ALTO:g} y al mínimo de {UMBRAL_MINIMO:g}."
            )
            respuesta = mejor_fragmento["texto"]

    return {
        "pregunta": pregunta,
        "workspace": workspace_id,
        "intencion": intencion,
        "especialista": especialista,
        "fragmentos": fragmentos,
        "veredicto": veredicto,
        "motivo": motivo,
        "respuesta": respuesta,
    }


# ---------------------------------------------------------------------------
# LA PÁGINA
#
# La página permite que un humano entienda de un vistazo qué hizo el asistente
# y por qué. Muestra como mínimo:
#
#   - la intención detectada
#   - los fragmentos recuperados, cada uno con su puntaje de similitud
#   - el veredicto, visualmente distinto en los tres casos
#   - la respuesta final, o el aviso de que no hay evidencia suficiente
#
# Debe quedar imposible confundir "esto está sustentado" con "esto no lo sé".
# ---------------------------------------------------------------------------

PAGINA = """<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<title>Consola del Asistente</title>
<style>
  body { font-family: system-ui, sans-serif; max-width: 820px; margin: 40px auto;
         padding: 0 20px; color: #1a2330; }
  input[type=text] { width: 100%; padding: 10px; font-size: 16px; }
  button { padding: 10px 18px; font-size: 15px; cursor: pointer; }
  #out { display: grid; gap: 16px; }
  .card { border: 1px solid #ccd5df; border-radius: 8px; padding: 14px; }
  .summary { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 8px; }
  .label { color: #51606f; font-size: 13px; font-weight: 700; text-transform: uppercase; }
  .verdict { border: 3px solid; font-size: 22px; font-weight: 800; }
  .verdict-APROBADO { background: #e8f7ed; border-color: #207a3d; color: #135328; }
  .verdict-DUDOSO { background: #fff5d6; border-color: #9a6800; color: #624300; }
  .verdict-SIN_EVIDENCIA { background: #fde8e7; border-color: #a52820; color: #721c18; }
  .fragment { background: #f5f7fa; }
  .selected { border: 3px solid #1769aa; }
  .meta { color: #51606f; font-size: 14px; }
  .abstention { color: #721c18; font-size: 18px; font-weight: 800; }
</style>
</head><body>
  <h1>Consola del Asistente</h1>

  <form id="f">
    <input type="text" id="q" placeholder="Escribe una pregunta…" autofocus>
    <p>
      <select id="ws">
        <option value="acme">acme</option>
        <option value="globex">globex</option>
        <option value="initech">initech</option>
      </select>
      <button type="submit">Preguntar</button>
    </p>
  </form>

  <main id="out" aria-live="polite">Escribe una pregunta para empezar.</main>

<script>
const node = (tag, text, className) => {
  const element = document.createElement(tag);
  if (text !== undefined && text !== null) element.textContent = String(text);
  if (className) element.className = className;
  return element;
};

const field = (label, value) => {
  const container = node('div');
  container.append(node('div', label, 'label'), node('div', value ?? '—'));
  return container;
};

const renderResult = (out, data) => {
  out.replaceChildren();

  const summary = node('section', undefined, 'card summary');
  summary.append(
    field('Pregunta', data.pregunta),
    field('Workspace', data.workspace),
    field('Intención', data.intencion),
    field('Especialista', data.especialista)
  );

  const verdictClass = {
    APROBADO: 'verdict-APROBADO',
    DUDOSO: 'verdict-DUDOSO',
    SIN_EVIDENCIA: 'verdict-SIN_EVIDENCIA'
  }[data.veredicto] || '';
  const verdict = node('section', undefined, `card verdict ${verdictClass}`);
  verdict.setAttribute('role', 'status');
  verdict.append(node('div', 'Veredicto', 'label'), node('div', data.veredicto));

  const evidence = node('section', undefined, 'card');
  evidence.append(node('h2', 'Fragmentos recuperados'));
  const selectedIndex = data.fragmentos.reduce(
    (best, fragment, index, all) =>
      best < 0 || fragment.similitud > all[best].similitud ? index : best,
    -1
  );
  data.fragmentos.forEach((fragment, index) => {
    const selected = index === selectedIndex;
    const item = node('article', undefined, `card fragment${selected ? ' selected' : ''}`);
    if (selected) item.append(node('strong', 'Fragmento seleccionado'));
    item.append(
      node('div', `Fuente: ${fragment.source_id} · Título: ${fragment.titulo} · Chunk: ${fragment.chunk}`, 'meta'),
      node('div', `Similitud: ${fragment.similitud}`, 'meta'),
      node('p', fragment.texto)
    );
    evidence.append(item);
  });
  if (!data.fragmentos.length) evidence.append(node('p', 'No se recuperaron fragmentos.'));

  const decision = node('section', undefined, 'card');
  decision.append(node('h2', 'Motivo'), node('p', data.motivo), node('h2', 'Respuesta'));
  decision.append(data.respuesta === null
    ? node('p', 'No hay evidencia suficiente para responder.', 'abstention')
    : node('p', data.respuesta));

  out.append(summary, verdict, evidence, decision);
};

document.getElementById('f').onsubmit = async (e) => {
  e.preventDefault();
  const q = document.getElementById('q').value;
  const ws = document.getElementById('ws').value;
  const out = document.getElementById('out');
  out.textContent = 'Consultando…';
  try {
    const r = await fetch(`/api/consulta?q=${encodeURIComponent(q)}&ws=${encodeURIComponent(ws)}`);
    const data = await r.json();
    renderResult(out, data);
  } catch (err) {
    out.textContent = 'Error: ' + err;
  }
};
</script>
</body></html>
"""


# ---------------------------------------------------------------------------
# SERVIDOR — ya funciona. Puedes tocarlo si lo necesitas, pero no hace falta.
# ---------------------------------------------------------------------------

class Handler(BaseHTTPRequestHandler):

    def _send(self, code, body, content_type):
        payload = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", f"{content_type}; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):
        url = urlparse(self.path)

        if url.path in ("/", "/index.html"):
            return self._send(200, PAGINA, "text/html")

        if url.path == "/api/consulta":
            params = parse_qs(url.query)
            pregunta = (params.get("q") or [""])[0]
            workspace = (params.get("ws") or ["acme"])[0]
            try:
                data = asyncio.run(consultar(pregunta, workspace))
                return self._send(200, json.dumps(data, ensure_ascii=False), "application/json")
            except NotImplementedError as exc:
                return self._send(
                    501, json.dumps({"error": str(exc)}, ensure_ascii=False),
                    "application/json")
            except Exception:
                logger.exception("fallo al consultar %r", pregunta)
                return self._send(
                    500, json.dumps({"error": "error interno, revisa la consola"},
                                    ensure_ascii=False), "application/json")

        self._send(404, json.dumps({"error": "no encontrado"}), "application/json")

    def log_message(self, fmt, *args):
        logger.info("%s", fmt % args)


if __name__ == "__main__":
    print(f"\n  Consola del Asistente  →  http://localhost:{PUERTO}\n")
    HTTPServer(("127.0.0.1", PUERTO), Handler).serve_forever()
