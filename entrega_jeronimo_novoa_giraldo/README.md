# Entrega — Prueba Técnica IA (Parte 2)

Esqueleto autocontenido de un asistente de IA sobre contenido propio de cada
cliente. **No necesitas credenciales de ninguna nube ni conexión a internet**:
la base de datos y el almacenamiento están reemplazados por dobles en memoria
que leen de `fixtures/`. La API que ves tiene la misma forma que una real.

## Puesta en marcha

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m pytest       # 61 pruebas deben aprobar
python app.py          # abre http://localhost:8000
```

La suite y la consola funcionan completamente en local. La aplicación no usa
credenciales, red externa ni servicios de IA. Para auditar los archivos
protegidos, las dependencias y el ledger pendiente, ejecuta también:

```bash
python -m tools.verify_delivery
```

Requiere Python 3.10 o superior.

## Mapa del repo

```
app.py                        Ejercicio 6 — consola y pipeline local completos
config/intents.py             Ejercicio 1 — catálogo y clasificación de intención
tools/intent_report_tool.py   Ejercicio 2 — reporte de cobertura por intención
tools/legacy_answers_tool.py  Ejercicio 3 — recuperación heredada corregida
prompts/verificador_v1.md     Ejercicio 4 — versión original preservada
prompts/verificador_v2.md     Ejercicio 4 — contrato estricto de verificación
tools/loop_guard.py           Ejercicio 5 — guardia anti-loop
shared/clients.py             Clientes (dobles). LÉELO ANTES DE EMPEZAR. No lo modifiques.
shared/retriever.py           Buscador de fragmentos. Te lo damos hecho. No lo modifiques.
fixtures/                     Datos de la base y del almacenamiento. No los modifiques.
tests/                        Suite completa de regresión
```

## Reglas

- **No modifiques** `shared/clients.py`, `shared/retriever.py`, `fixtures/`,
  `pytest.ini` ni `tests/test_classify_intent.py`. Todo lo demás es tuyo.
- **No agregues dependencias.** `requirements.txt` no debe crecer.
- Puedes agregar archivos y módulos si lo necesitas.
- Puedes usar asistentes de IA. Debes declararlo en `NOTAS.md` y vas a tener que
  defender cada línea en la sesión de revisión.

El enunciado original está en `../02_Prueba_Practica.pdf` desde el directorio
de entrega ubicado en la raíz del repositorio.
