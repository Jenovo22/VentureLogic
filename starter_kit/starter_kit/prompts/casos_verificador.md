# Casos esperados del verificador v2

Matriz reconciliada con `fixtures/db.json`; los textos citados se comparan como subcadenas exactas de la fuente indicada.

| Respuesta | Cita literal | Fuente válida | Trazabilidad completa | Similitud suficiente | Veredicto | Motivo |
|---|---:|---:|---:|---:|---|---|
| `a-1` | Sí | Sí (`src-1`) | Sí (`chunk` 3) | Sí (`0.91`) | `APROBADO` | La cita aparece literalmente en `src-1`, el chunk está identificado y `0.91 >= 0.75`. |
| `a-2` | No | Sí (`src-1`) | Sí (`chunk` 0) | No (`0.34`) | `RECHAZADO` | La cita genérica no aparece literalmente en `src-1` y `0.34 < 0.55`. |
| `a-3` | No | Sí (`src-2`) | Sí (`chunk` 7) | Sí (`0.88`) | `RECHAZADO` | `Configuración > Equipo` no es texto literal de `Configuración, luego a Equipo`; falla aunque `src-2` sea válida y la similitud sea `0.88`. |
| `a-4` | No verificable | No (`src-99-inexistente`) | No | Sí (`0.79`) | `RECHAZADO` | La fuente declarada no existe, por lo que se rechaza antes de considerar trazabilidad o similitud. |
| `a-5` | Sí | Sí (`src-1`) | No (`chunk` nulo) | Sí (`0.86`) | `DUDOSO` | La cita literal y `0.86` son utilizables, pero falta el chunk requerido para trazabilidad completa. |

No se modificó ninguna fixture ni fuente para obtener estos resultados.
