# Notas de entrega — INCOMPLETO: nombre pendiente de la persona candidata

## Resumen

- Estado general: **INCOMPLETO**. Se completaron los cortes del clasificador y del reporte de cobertura por intención.
- Completado: `classify_intent()` y `count_messages_by_intent()` conforme a sus contratos.
- Pendiente: ejercicios 3 a 6, auditoría final, evidencia de consola y verificación desde un clon nuevo.
- Motivo: la entrega se construye en cortes autónomos para preservar evidencia y facilitar la revisión.

## Tiempo

| Dato | Estado |
|---|---|
| Inicio real | **INCOMPLETO — pendiente de dato proporcionado por la persona candidata** |
| Entrega real | **INCOMPLETO — todavía no ocurrió** |
| Ejercicio 1 | **INCOMPLETO — horas reales pendientes** |
| Ejercicio 2 | Implementación completada; **INCOMPLETO — horas reales pendientes** |
| Ejercicio 3 | **INCOMPLETO — no iniciado** |
| Ejercicio 4 | **INCOMPLETO — no iniciado** |
| Ejercicio 5 | **INCOMPLETO — no iniciado** |
| Ejercicio 6 | **INCOMPLETO — no iniciado** |

## Decisiones

### Alta confianza

1. Normalizar el texto elegible una sola vez con NFKD y eliminar marcas combinantes. Evita duplicar reglas por patrón y mantiene el clasificador dirigido por catálogo.
2. Excluir líneas citadas antes de normalizar. Así, el contenido de conversaciones anteriores no puede decidir la intención actual.
3. Reemplazar el resultado solo ante un patrón estrictamente más largo. Esto resuelve especificidad y conserva el orden del catálogo en empates.

### Baja confianza

1. **INCOMPLETO — pendiente de una decisión real y de la evidencia que justificaría revertirla.**
2. **INCOMPLETO — pendiente de una decisión real y de la evidencia que justificaría revertirla.**

## Ejercicio 1 — reglas vs LLM

Las reglas ofrecen resultados deterministas, rápidos y auditables: ante el mismo catálogo y mensaje siempre producen la misma intención, sin costo de inferencia ni dependencia externa. Su desventaja es que la cobertura depende de frases previstas; variaciones semánticas no representadas pueden quedar como desconocidas. Cambiaría a un clasificador entrenado o a un LLM cuando los mensajes reales mostraran una tasa sostenida de desconocidos o errores por paráfrasis que hiciera inmantenible ampliar el catálogo. Antes del cambio mediría esa tasa con el reporte de cobertura y conservaría un conjunto de evaluación, límites de confianza y una salida desconocida para evitar convertir mayor cobertura en decisiones opacas e inseguras.

## Ejercicio 3 — tabla de defectos

**INCOMPLETO — el ejercicio 3 todavía no fue revisado ni corregido.**

| # | Línea | Qué está mal | Síntoma en producción | Gravedad |
|---|---|---|---|---|
| — | — | Pendiente de análisis | Pendiente de evidencia | Pendiente |

## Ejercicio 4 — qué movería a código determinista

**INCOMPLETO — nota pendiente hasta implementar y evaluar el verificador v2 (máximo 120 palabras).**

## Ejercicio 6 — cómo mejoraría el recuperador

**INCOMPLETO — nota pendiente hasta implementar y evaluar la consola (máximo 120 palabras).**

## Ejercicio 5 — dónde enchufo la guardia

**INCOMPLETO — nota pendiente hasta implementar y evaluar la guardia (máximo 150 palabras).**

## Uso de IA

**INCOMPLETO — la persona candidata debe declarar la herramienta utilizada, los ejercicios afectados y el uso exacto. No se presupone ni fabrica esa declaración.**

## Evidencia de verificación

- Recolección inicial: 21 pruebas detectadas.
- RED inicial del clasificador: 18 fallos por `NotImplementedError`.
- GREEN del clasificador: 18 pruebas aprobadas.
- Suite completa posterior: 18 aprobadas y 3 fallidas. Los fallos restantes corresponden a `consultar()` (2) y `count_messages_by_intent()` (1), todavía no implementados.
- Integridad posterior: todos los hashes protegidos coinciden; el literal fuente y el hash canónico de `INTENTS` coinciden con la línea base.
- RED del reporte: 8 fallos en 0.08 s antes de implementar el comportamiento.
- GREEN del reporte: 8 pruebas aprobadas en 0.05 s; la suite completa quedó en 26 aprobadas y 2 fallidas por `consultar()`, fuera de este corte.

## Captura de abstención Enterprise

**INCOMPLETO — pendiente de una captura real de la consola final en ejecución. No se adjunta evidencia fabricada.**

## Qué haría con una semana más

**INCOMPLETO — pendiente de completar a partir de los resultados finales y limitaciones observadas.**

## Registro por cortes

### Corte 1 — clasificador y procedencia

- Se creó una línea base Git separada antes de editar código fuente.
- Se registraron hashes SHA-256 de los archivos protegidos y del literal canónico `INTENTS`.
- La normalización elimina citas, descompone Unicode, elimina marcas, convierte signos en espacios y colapsa separadores.
- La coincidencia usa límites de token, selecciona el patrón más largo y conserva el orden del catálogo en empates.
- Estado de pruebas: 18/18 pruebas enfocadas aprobadas; la suite completa conserva 3 fallos esperados por ejercicios todavía pendientes.
- Tamaño authored del corte funcional: 143 líneas añadidas o eliminadas, sin contar los artefactos OpenSpec de progreso.

### Corte 2 — reporte de cobertura por intención

- Se reutilizan exclusivamente `get_db_client()` y `get_storage_client()`; dos reportes consecutivos mantienen una sola instancia de cada cliente.
- Un workspace inexistente conserva el `KeyError` del almacenamiento porque no equivale a un workspace existente sin mensajes.
- Los resultados inactivos o no registrados se acumulan en `desconocido`; así, la suma siempre coincide con los mensajes recuperados.
- Los errores operativos se propagan y registran solo la operación y el workspace, sin cuerpos de mensajes, credenciales ni texto de la excepción.
- Evidencia temporal del runner: RED 8 fallos en 0.08 s; GREEN 8 aprobadas en 0.05 s. Estas duraciones no sustituyen las horas reales, que siguen pendientes.
