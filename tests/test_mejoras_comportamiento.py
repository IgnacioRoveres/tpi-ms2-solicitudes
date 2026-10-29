"""Cambios de comportamiento INTENCIONALES (mejoras de calidad externa).

En la version inicial estos casos fallaban (ver docs/diagnostico.md, S7 y S8).
No forman parte del golden master porque ahi el comportamiento era un error.
"""
import subprocess
import sys

from tests.caracterizacion.ejecutor import PROGRAMA, ejecutar
from tests.caracterizacion.escenarios import ALTA_ANA


def test_id_no_numerico_no_corta_el_programa():
    resultado = ejecutar(ALTA_ANA + ["2", "abc", "3", "uno", "0"])
    assert resultado["codigo_salida"] == 0
    assert resultado["salida"].count("Error: el ID debe ser un numero") == 2
    assert "Traceback" not in resultado["salida"]
    assert resultado["salida"].rstrip().endswith("Hasta luego")


def test_responsable_no_numerico_se_informa_como_invalido():
    resultado = ejecutar(ALTA_ANA + ["3", "1", "dos", "0"])
    assert "Error: responsable invalido" in resultado["salida"]
    assert resultado["datos"]["solicitudes"][0]["responsable"] is None


def test_archivo_danado_no_se_sobrescribe(tmp_path):
    archivo = tmp_path / "solicitudes.json"
    contenido_danado = '{"estudiantes": {}, "solicitudes": [{"id": 1'
    archivo.write_text(contenido_danado, encoding="utf-8")
    proceso = subprocess.run(
        [sys.executable, str(PROGRAMA)],
        input="\n".join(ALTA_ANA + ["0"]) + "\n",
        capture_output=True, text=True, cwd=tmp_path, timeout=20,
    )
    assert proceso.returncode == 1
    assert "esta danado" in proceso.stdout
    assert archivo.read_text(encoding="utf-8") == contenido_danado
