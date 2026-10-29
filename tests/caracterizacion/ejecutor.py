"""Ejecuta el programa como caja negra y captura lo observable."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
PROGRAMA = RAIZ / "sistema.py"
CARPETA_GOLDEN = Path(__file__).parent / "golden"


def ejecutar(entradas):
    """Corre `python sistema.py` en una carpeta vacia con las entradas dadas.

    Devuelve un dict con la salida por pantalla y los datos persistidos
    (sin el campo `fecha`, que depende del dia de ejecucion).
    """
    with tempfile.TemporaryDirectory() as carpeta:
        proceso = subprocess.run(
            [sys.executable, str(PROGRAMA)],
            input="\n".join(entradas) + "\n",
            capture_output=True,
            text=True,
            cwd=carpeta,
            timeout=20,
        )
        archivo = Path(carpeta) / "solicitudes.json"
        datos = json.loads(archivo.read_text(encoding="utf-8")) if archivo.exists() else None
    if datos:
        for solicitud in datos["solicitudes"]:
            solicitud.pop("fecha", None)
    return {"codigo_salida": proceso.returncode, "salida": proceso.stdout, "datos": datos}
