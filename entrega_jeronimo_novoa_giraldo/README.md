# Entrega — Prueba Técnica IA (Parte 2)

Esqueleto autocontenido de un asistente de IA sobre contenido propio de cada
cliente. **No necesitas credenciales de ninguna nube ni conexión a internet**:
la base de datos y el almacenamiento están reemplazados por dobles en memoria
que leen de `fixtures/`. La API que ves tiene la misma forma que una real.

## Puesta en marcha

Requiere Python 3.10 o superior. Los siguientes pasos parten desde la raíz del
repositorio clonado, donde se encuentran `02_Prueba_Practica.pdf` y la carpeta
`entrega_jeronimo_novoa_giraldo/`.

Si todavía no tienes el repositorio:

```bash
git clone https://github.com/Jenovo22/VentureLogic.git
cd VentureLogic
```

Si ya lo tienes, abre una terminal en su raíz antes de continuar.

### Linux

```bash
cd entrega_jeronimo_novoa_giraldo
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

En Linux, que `python` no exista antes de crear el entorno es normal: usa
`python3` para crearlo. Después de activarlo, los comandos `python` y `pip`
apuntan al entorno virtual, no a la instalación global.

Si Debian o Ubuntu indican que no se pudo crear el entorno virtual, instala el
soporte del sistema y repite los pasos anteriores:

```bash
sudo apt update
sudo apt install python3-venv
```

No uses `sudo pip` ni `--break-system-packages`: los paquetes siempre se
instalan dentro del `.venv` del proyecto.

### macOS

```bash
cd entrega_jeronimo_novoa_giraldo
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

En macOS, `python3` suele estar disponible tras instalar Python desde
`https://www.python.org/downloads/` o con Homebrew (`brew install python`).
Al igual que en Linux, crea el entorno con `python3` y, una vez activado, usa
`python` y `python -m pip` dentro del entorno virtual.

### Windows PowerShell

```powershell
cd .\entrega_jeronimo_novoa_giraldo
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Si PowerShell bloquea el script de activación, habilítalo solo para la sesión
actual y vuelve a activarlo:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### Windows CMD

```bat
cd entrega_jeronimo_novoa_giraldo
py -3 -m venv .venv
.venv\Scripts\activate.bat
python -m pip install -r requirements.txt
```

En Windows, si `py` no está disponible, instala Python 3 desde
`https://www.python.org/downloads/` con Python Launcher habilitado.

### Verificar y ejecutar

Con el entorno virtual activo, el prompt muestra `(.venv)`. Ejecuta estos
comandos desde `entrega_jeronimo_novoa_giraldo/` en cualquiera de los sistemas:

```bash
python -m pytest
python -m tools.verify_delivery
python app.py
```

Las 61 pruebas deben aprobar y el verificador debe terminar con código 0. Abre
`http://localhost:8000` para usar la consola y presiona `Ctrl+C` en la terminal
para detener el servidor.

La suite y la consola funcionan completamente en local. La aplicación no usa
credenciales, red externa ni servicios de IA.

## Estructura del repositorio

Desde la raíz del clon:

```
VentureLogic/
├── 02_Prueba_Practica.pdf          Enunciado original de la prueba
└── entrega_jeronimo_novoa_giraldo/ Paquete entregable y autocontenido
    ├── README.md                   Esta guía de puesta en marcha
    ├── NOTAS.md                    Notas de entrega exigidas por la prueba
    ├── app.py                      Ejercicio 6 — consola y pipeline local
    ├── pytest.ini                  Configuración de la suite de pruebas
    ├── requirements.txt            Dependencias (pytest y pytest-asyncio)
    ├── config/
    │   └── intents.py              Ejercicio 1 — catálogo y clasificación
    ├── tools/
    │   ├── intent_report_tool.py   Ejercicio 2 — reporte de cobertura
    │   ├── legacy_answers_tool.py  Ejercicio 3 — recuperación corregida
    │   ├── loop_guard.py           Ejercicio 5 — guardia anti-loop
    │   ├── correction_ledger.py    Registro de correcciones pendientes
    │   └── verify_delivery.py      Verificador de integridad de la entrega
    ├── prompts/
    │   ├── verificador_v1.md       Ejercicio 4 — prompt original
    │   ├── verificador_v2.md       Ejercicio 4 — contrato estricto
    │   └── casos_verificador.md    Casos esperados del verificador
    ├── shared/
    │   ├── clients.py              Dobles de clientes (no modificar)
    │   └── retriever.py            Buscador léxico (no modificar)
    ├── fixtures/
    │   ├── db.json                 Base de datos de prueba (no modificar)
    │   └── storage.json            Almacenamiento de prueba (no modificar)
    ├── evidence/
    │   ├── enterprise-abstention.png       Captura de la abstención Enterprise
    │   ├── protected_baseline.json         Hashes de archivos protegidos
    │   └── pending_source_corrections.jsonl Ledger de fuentes pendientes
    └── tests/                      Suite completa de regresión (61 pruebas)
```

Qué contiene cada sección:

| Ruta | Qué es | Ejercicio / uso |
|------|--------|-----------------|
| `app.py` | Servidor y pipeline `consultar()` con la consola web | Ejercicio 6; se ejecuta con `python app.py` |
| `config/intents.py` | Catálogo `INTENTS` y `classify_intent()` por reglas | Ejercicio 1 |
| `tools/intent_report_tool.py` | Conteo asíncrono de mensajes por intención | Ejercicio 2 |
| `tools/legacy_answers_tool.py` | Recuperación heredada corregida | Ejercicio 3 |
| `tools/loop_guard.py` | Límite de llamadas por (sesión, agente) | Ejercicio 5 |
| `tools/correction_ledger.py` | Ledger de correcciones de fuente pendiente | Soporte del Ejercicio 3 |
| `tools/verify_delivery.py` | Verifica hashes, `INTENTS` y dependencias | Auditoría con `python -m tools.verify_delivery` |
| `prompts/` | Contrato del verificador y sus casos | Ejercicio 4 |
| `shared/` | Dobles de clientes y buscador provistos | Leer antes de empezar; no modificar |
| `fixtures/` | Datos de prueba de base y almacenamiento | No modificar |
| `evidence/` | Captura, baseline de integridad y ledger | Evidencia evaluable de la entrega |
| `tests/` | Pruebas de regresión de todos los ejercicios | Se ejecutan con `python -m pytest` |
| `NOTAS.md` | Resumen, tiempos, decisiones y uso de IA | Documento obligatorio de la prueba |

## Reglas

- **No modifiques** `shared/clients.py`, `shared/retriever.py`, `fixtures/`,
  `pytest.ini` ni `tests/test_classify_intent.py`. Todo lo demás es tuyo.
- **No agregues dependencias.** `requirements.txt` no debe crecer.
- Puedes agregar archivos y módulos si lo necesitas.
- Puedes usar asistentes de IA. Debes declararlo en `NOTAS.md` y vas a tener que
  defender cada línea en la sesión de revisión.

El enunciado original está en `../02_Prueba_Practica.pdf` desde el directorio
de entrega ubicado en la raíz del repositorio.
