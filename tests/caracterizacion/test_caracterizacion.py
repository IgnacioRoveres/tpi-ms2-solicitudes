"""Pruebas de caracterizacion: el comportamiento externo no debe cambiar.

Compara, escenario por escenario, la salida por pantalla y los datos
guardados contra la referencia grabada sobre la version inicial.
"""
import json

import pytest

from tests.caracterizacion.ejecutor import CARPETA_GOLDEN, ejecutar
from tests.caracterizacion.escenarios import ESCENARIOS


@pytest.mark.parametrize("nombre", sorted(ESCENARIOS))
def test_comportamiento_igual_a_version_inicial(nombre):
    esperado = json.loads((CARPETA_GOLDEN / f"{nombre}.json").read_text(encoding="utf-8"))
    obtenido = ejecutar(ESCENARIOS[nombre])
    assert obtenido["salida"] == esperado["salida"]
    assert obtenido["datos"] == esperado["datos"]
    assert obtenido["codigo_salida"] == esperado["codigo_salida"]
