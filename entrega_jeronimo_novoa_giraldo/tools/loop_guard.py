"""
EJERCICIO 5 — Guardia contra loops de agentes.

Problema real: un agente entra en bucle llamando a la misma herramienta una y
otra vez (típicamente la que escribe en el estado compartido). Un loop no se ve
como un crash: se ve como una factura del proveedor de modelos que se dispara y
una petición que nunca termina. Ya existe una instrucción en el prompt pidiendo
al agente que no lo haga, pero un prompt es una sugerencia, no un control.

Necesitamos una guardia en código.
"""

from __future__ import annotations

import logging
import threading

logger = logging.getLogger(__name__)

MAX_CALLS = 3


class ToolLoopError(RuntimeError):
    """Se levanta cuando un agente supera el límite de llamadas a una herramienta."""


class LoopGuard:
    """Cuenta llamadas por (sesión, agente) y aborta al excederse.

    Requisitos:

    - `record(session_id, agent_name)` registra una llamada y devuelve el
      conteo actualizado.
    - A la llamada número `MAX_CALLS + 1` del **mismo agente en la misma
      sesión**, levanta `ToolLoopError` con un mensaje que incluya el nombre
      del agente, el id de sesión y el conteo. Un mensaje que solo diga "loop
      detectado" no sirve a las 3 a.m.
    - Los conteos son independientes por agente y por sesión: que `classifier`
      llame 3 veces en la sesión A no afecta a `verifier` ni a la sesión B.
    - `reset(session_id)` limpia los conteos de una sesión terminada. Sin esto,
      un proceso de larga vida acumula memoria durante horas.
    - `snapshot(session_id)` devuelve `{agente: conteo}` para poder loguearlo.

    Piensa en la concurrencia: los especialistas corren en paralelo dentro del
    mismo proceso. Documenta en un comentario si tu implementación es segura y
    por qué (o por qué no hace falta que lo sea).
    """

    def __init__(self, max_calls: int = MAX_CALLS):
        self._max_calls = max_calls
        self._counts: dict[tuple[str, str], int] = {}
        # Un único lock vuelve atómicas las transiciones del estado compartido.
        # La guardia no ejecuta trabajo externo dentro de la sección crítica.
        self._lock = threading.Lock()

    def record(self, session_id: str, agent_name: str) -> int:
        key = (session_id, agent_name)
        with self._lock:
            attempted_count = self._counts.get(key, 0) + 1
            if attempted_count > self._max_calls:
                raise ToolLoopError(
                    "Límite de llamadas excedido: "
                    f"session={session_id!r}, agent={agent_name!r}, "
                    f"count={attempted_count}, limit={self._max_calls}"
                )
            self._counts[key] = attempted_count
            return attempted_count

    def reset(self, session_id: str) -> None:
        with self._lock:
            keys = [key for key in self._counts if key[0] == session_id]
            for key in keys:
                del self._counts[key]

    def snapshot(self, session_id: str) -> dict[str, int]:
        with self._lock:
            snapshot = {
                agent_name: count
                for (stored_session, agent_name), count in self._counts.items()
                if stored_session == session_id
            }
        return snapshot
