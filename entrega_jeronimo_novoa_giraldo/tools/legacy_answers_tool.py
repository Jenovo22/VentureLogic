"""
EJERCICIO 3 — Código heredado con defectos.

Esta herramienta la escribió alguien con prisa y pasó a producción. Funciona
"en la mayoría de los casos", que es exactamente el problema.

Tu trabajo: encontrar los defectos, corregirlos y explicar cada uno.
NO reescribas la herramienta cambiando su propósito: debe seguir devolviendo
las respuestas de un workspace enriquecidas con el texto de su fuente.
"""

import logging

from shared.clients import get_db_client
from tools.correction_ledger import DEFAULT_LEDGER, PendingCorrectionLedger

logger = logging.getLogger(__name__)


async def get_workspace_answers(
    workspace_id: str,
    min_similitud: float = 0.0,
    *,
    ledger: PendingCorrectionLedger = DEFAULT_LEDGER,
) -> list[dict]:
    """Return fresh valid answers enriched from one batched source read."""
    db = get_db_client()

    answer_records = await db.table("answers").where("workspace_id", workspace_id).get()
    eligible = []
    for record in answer_records:
        answer = record.to_dict()
        if answer.get("similitud", 0.0) >= min_similitud:
            eligible.append((record.id, answer))
    if not eligible:
        return []

    source_records = await db.table("sources").get()
    sources = {record.id: record for record in source_records}
    result = []
    for answer_id, answer in eligible:
        source_id = answer.get("source_id")
        source_record = sources.get(source_id)
        reason = None
        detail = None

        if source_record is None:
            reason = "missing_source"
            detail = "Referenced source was not found."
        else:
            try:
                source = source_record.to_dict()
            except (TypeError, ValueError):
                reason = "malformed_source"
                detail = "Referenced source could not be decoded as a record."
            else:
                if not isinstance(source, dict):
                    reason = "malformed_source"
                    detail = "Referenced source is not an object."
                elif not isinstance(source.get("titulo"), str) or not source["titulo"].strip():
                    reason = "missing_title"
                    detail = "Referenced source has no non-empty title."

        if reason is not None:
            logger.warning(
                "legacy answer omitted: workspace=%s answer=%s source=%s reason=%s",
                workspace_id,
                answer_id,
                source_id,
                reason,
            )
            ledger.record(
                {
                    "workspace_id": workspace_id,
                    "answer_id": answer_id,
                    "source_id": source_id,
                    "reason": reason,
                    "detail": detail,
                }
            )
            continue

        enriched = dict(answer)
        enriched["fuente_titulo"] = source["titulo"]
        enriched["confianza"] = "alta" if answer["similitud"] > 0.8 else "baja"
        result.append(enriched)

    return result
