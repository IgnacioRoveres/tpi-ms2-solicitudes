"""Graba la salida de referencia (golden master) de la version actual.

Se ejecuto UNA sola vez sobre el tag `estado-inicial`, antes de refactorizar:
    python -m tests.caracterizacion.grabar_golden
No volver a ejecutar despues del refactoring: la referencia es la version base.
"""
import json

from tests.caracterizacion.ejecutor import CARPETA_GOLDEN, ejecutar
from tests.caracterizacion.escenarios import ESCENARIOS

if __name__ == "__main__":
    CARPETA_GOLDEN.mkdir(exist_ok=True)
    for nombre, entradas in ESCENARIOS.items():
        resultado = ejecutar(entradas)
        destino = CARPETA_GOLDEN / f"{nombre}.json"
        destino.write_text(json.dumps(resultado, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"grabado {destino.name}")
