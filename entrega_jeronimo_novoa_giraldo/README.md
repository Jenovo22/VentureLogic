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

### Linux y macOS

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

No uses `sudo pip` ni `--break-system-packages`.

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
