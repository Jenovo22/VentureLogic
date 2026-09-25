# Notas de entrega — INCOMPLETO: nombre pendiente de la persona candidata

## Resumen

- Estado general: **INCOMPLETO**. Se completaron el clasificador, el reporte por intención, la recuperación heredada, el verificador v2 y la consola del ejercicio 6.
- Completado: `classify_intent()`, `count_messages_by_intent()`, la recuperación aislada con registro de correcciones, el verificador v2 no reescritor, la orquestación asíncrona y la interfaz segura de evidencia.
- Pendiente: ejercicio 5, auditoría final, captura de pantalla y verificación desde un clon nuevo.
- Motivo: la entrega se construye en cortes autónomos para preservar evidencia y facilitar la revisión.

## Tiempo

| Dato | Estado |
|---|---|
| Inicio real | **INCOMPLETO — pendiente de dato proporcionado por la persona candidata** |
| Entrega real | **INCOMPLETO — todavía no ocurrió** |
| Ejercicio 1 | **INCOMPLETO — horas reales pendientes** |
| Ejercicio 2 | Implementación completada; **INCOMPLETO — horas reales pendientes** |
| Ejercicio 3 | Implementación completada; **INCOMPLETO — horas reales pendientes** |
| Ejercicio 4 | Implementación documental completada; **INCOMPLETO — horas reales pendientes** |
| Ejercicio 5 | **INCOMPLETO — no iniciado** |
| Ejercicio 6 | Núcleo e interfaz completados; **INCOMPLETO — horas reales y captura final pendientes** |

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

| # | Línea | Qué está mal | Síntoma en producción | Gravedad |
|---|---|---|---|---|
| 1 | `tools/legacy_answers_tool.py`, firma original | El argumento `cache={}` conserva resultados mutables por proceso y solo usa el workspace como clave. | Solicitudes posteriores reciben datos de otro umbral y observan mutaciones hechas por llamantes anteriores. | Crítica |
| 2 | `tools/legacy_answers_tool.py`, construcción original del cliente | Cada ejecución construye `DatabaseClient()` en lugar de reutilizar el singleton suministrado. | Aumentan conexiones e inicializaciones y se rompe el contrato de una instancia por proceso. | Alta |
| 3 | `tools/legacy_answers_tool.py`, bucle original de fuentes | Se realiza una lectura secuencial de fuente por cada respuesta antes de completar la solicitud. | La latencia crece linealmente y fuentes repetidas generan lecturas redundantes. | Alta |
| 4 | `tools/legacy_answers_tool.py`, escritura original | Cada solicitud sobrescribe `/tmp/last_answers.json` como estado compartido. | Solicitudes concurrentes filtran o pisan respuestas entre sí y dependen de un efecto lateral global. | Crítica |
| 5 | `tools/legacy_answers_tool.py`, resolución original de fuente | Una fuente inexistente, malformada o sin título aborta la solicitud completa sin evidencia durable. | Una respuesta defectuosa oculta respuestas válidas y el defecto no queda disponible para corrección auditada. | Alta |

La implementación elimina el caché y la salida temporal, obtiene respuestas y fuentes una vez por solicitud, aplica el umbral inclusivo antes de leer fuentes y devuelve diccionarios nuevos. Las respuestas con fuente inválida se omiten; el registro pendiente conserva identificadores y motivo sin ampliar el esquema devuelto ni modificar datos protegidos.

## Ejercicio 4 — qué movería a código determinista

Movería a código determinista la validación del esquema, la pertenencia de la fuente, la comparación literal de la cita, la presencia y coincidencia del chunk, los límites numéricos y la precedencia del veredicto. Son reglas cerradas, auditables y sensibles a valores exactos; un LLM puede variarlas o aceptar paráfrasis plausibles. Reservaría el LLM para explicar en lenguaje natural un resultado ya calculado, nunca para alterar los booleanos ni reescribir la respuesta. Incluso esa explicación quedaría restringida a los hechos observados. Así, el mismo JSON produce siempre el mismo veredicto y casos como una fuente inexistente, una cita no literal o una similitud exactamente igual a `0.55` no dependen del juicio probabilístico del modelo.

## Ejercicio 6 — cómo mejoraría el recuperador

Cambiaría la comparación léxica por recuperación semántica con embeddings: representaría preguntas y fragmentos como vectores y buscaría por cercanía, de modo que “restablecer contraseña” y “recuperar acceso” puedan coincidir aunque no compartan palabras. Mantendría un índice léxico como señal complementaria para términos exactos, nombres de planes y cifras. El costo es mayor complejidad operativa: generar y versionar embeddings, reconstruir el índice cuando cambia el contenido, medir latencia y pagar cómputo o un servicio externo. También exigiría un conjunto de evaluación por cliente para ajustar umbrales y comprobar que la mejora semántica no recupera fragmentos plausibles pero incorrectos.

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
- RED de `consultar()`: 9 fallos en 0.11 s antes de implementar el núcleo.
- GREEN de `consultar()`: 9 pruebas aprobadas en 0.04 s; regresiones de clasificador y reporte aprobadas, y suite completa 35/35 en 0.08 s.
- Smoke HTTP del corte: `/api/consulta` devolvió 200, las 8 claves exactas, 4 fragmentos, `APROBADO` y la respuesta literal del fragmento con mayor similitud.
- RED de interfaz segura: 3 fallos esperados antes de reemplazar el volcado JSON.
- GREEN de interfaz: 12/12 pruebas de `test_app.py`; regresiones de clasificador 18/18 y reporte 8/8; suite completa 38/38.
- Demostración HTTP real: Pro → `APROBADO` (1.0), contraseña → `DUDOSO` (0.566), Enterprise → `SIN_EVIDENCIA` (0.373, respuesta nula); cuatro fragmentos en cada caso.
- Prueba hostil HTTP: pregunta con `<img onerror>` y `<script>` y workspace con `<script>` conservaron el texto exacto en JSON; la página usa `createElement`/`textContent`, no contiene `innerHTML` y codifica ambos parámetros.
- Limitación: no había navegador ni automatización disponible; se usaron contratos estáticos, pruebas de página y tráfico HTTP real. La captura final sigue pendiente para el corte 8.
- RED de recuperación heredada: 11 casos ejecutados contra el código original; 9 fallaron y 2 pasaron en 0.15 s. Los fallos expusieron contaminación por caché, pérdida de propiedad, lecturas de fuente y ausencia del ledger; los dos pases iniciales motivaron reforzar los escenarios de singleton y salida temporal antes de GREEN.
- Efecto lateral durante ese RED: la implementación heredada creó `/tmp/last_answers.json`. Su contenido no se leyó. Con autorización específica, el proceso padre eliminó ese archivo y verificó su ausencia; esta recuperación no autoriza acceso a otras rutas externas.
- GREEN del corte 5: 11/11 pruebas de ledger y recuperación aprobaron en 0.06 s. El ledger predeterminado registró el defecto real `a-4`/`src-99-inexistente` como `missing_source`; dos respuestas válidas de `acme` se conservaron.
- Verificador v2: los 2 ejemplos JSON se parsearon con claves cerradas; la matriz derivada directamente de la fixture fue `a-1` APROBADO, `a-2`/`a-3`/`a-4` RECHAZADO y `a-5` DUDOSO.
- Regresión del corte 6: suite completa 49/49 en 0.10 s; 7/7 hashes protegidos, `INTENTS`, dependencias, v1 y el informe histórico permanecieron sin cambios.

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

### Corte 3 — núcleo asíncrono de consulta

- `workspace_id` se devuelve como metadato de la solicitud; no filtra el recuperador protegido, cuya API global se conserva sin cambios.
- Todos los fragmentos se copian y mantienen en el orden recuperado; el veredicto y la respuesta usan el máximo real aunque la entrada no esté ordenada.
- Los límites se comparan sin redondear: menos de `0.55` abstiene, desde `0.55` hasta menos de `0.75` es `DUDOSO`, y desde `0.75` es `APROBADO`.
- Cada motivo expone el valor observado o la ausencia de fragmentos y los umbrales aplicables; la respuesta aprobada o dudosa conserva exactamente el texto superior.
- La interfaz existente no se modificó: el renderizado seguro y la demostración visual pertenecen al corte 4.

### Corte 4 — consola segura y legible

- La página crea nodos DOM y asigna pregunta, workspace, intención, especialista, fuentes, títulos, chunks, textos, puntajes, motivo y respuesta mediante `textContent`; ningún dato de respuesta se interpola como HTML.
- Pregunta y workspace se envían con `encodeURIComponent`. Los tres veredictos tienen estilos inequívocos, el fragmento con mayor puntaje queda marcado y la respuesta nula muestra una abstención explícita.
- El servidor local devolvió los tres resultados exigidos: Pro `APROBADO` con 1.0, contraseña `DUDOSO` con 0.566 y Enterprise `SIN_EVIDENCIA` con 0.373 y respuesta nula.
- La prueba hostil preservó literalmente sintaxis `<img onerror>` y `<script>` en la API sin insertarla en la plantilla. No había motor de navegador para ejecutar el DOM; la evidencia combina el contrato automatizado y HTTP real.
- No se tomó la captura Enterprise: permanece reservada para la verificación final del corte 8.

### Corte 5 — recuperación heredada y ledger pendiente

- El trabajo se dividió una sola vez: 5a contiene la infraestructura JSONL y sus pruebas; 5b integra la recuperación y sus pruebas para mantener unidades revisables.
- `get_workspace_answers()` reutiliza el singleton, consulta respuestas una vez, retorna temprano sin leer fuentes cuando no hay elegibles y carga la tabla de fuentes una sola vez para indexarla por identificador.
- Cada resultado y diccionario enriquecido es nuevo. El umbral es inclusivo y `confianza` conserva el contrato existente (`alta` solo cuando la similitud es mayor que `0.8`).
- Una fuente ausente, malformada o sin título genera log y registro durable con motivo distinto; la respuesta afectada se omite y las respuestas válidas conservan su esquema y disponibilidad.
- El ledger UTF-8 JSONL usa deduplicación estable, bloqueo de hilo, `flush`/`fsync`, estado `pending` y tiempo UTC. Un archivo ausente o vacío equivale a cero pendientes; sintaxis malformada falla explícitamente.
- El registro predeterminado contiene un defecto real de la fixture: respuesta `a-4`, fuente `src-99-inexistente`, motivo `missing_source`. Permanece pendiente y **no autoriza** corregir fuentes, fixtures ni datos.
- El RED inicial ejecutado contra la implementación heredada creó accidentalmente `/tmp/last_answers.json`; no se leyó su contenido. El proceso padre, con autorización específica para esa ruta, lo eliminó y verificó su ausencia. Las pruebas finales inspeccionan e interceptan el intento mediante mock, usan directorios temporales locales explícitos y no vuelven a sondear esa ruta real.

### Corte 6 — verificador v2 y matriz de fixtures

- El contrato exige respuesta, cita, fuente, chunk, similitud y evidencia autoritativa; devuelve solo el veredicto JSON cerrado y nunca una respuesta reescrita.
- La cita debe ser una subcadena literal, sin normalización ni aceptación de paráfrasis. Por eso `a-3` es `RECHAZADO` aunque use `src-2` y tenga similitud `0.88`.
- La precedencia rechaza primero fuentes inválidas y citas no literales. Evidencia válida desde `0.55` hasta menos de `0.75`, o evidencia real sin chunk, queda `DUDOSO`; desde `0.75` solo se aprueba si todos los controles pasan.
- La matriz queda: `a-1` APROBADO; `a-2`, `a-3` y `a-4` RECHAZADO; `a-5` DUDOSO. Las fixtures permanecen intactas.
