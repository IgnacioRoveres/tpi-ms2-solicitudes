from datetime import date

from sgsa.dominio import Estado, TipoSolicitud
from sgsa.dto import NuevaSolicitud
from sgsa.formato import formatear_resumen
from sgsa.modelos import Solicitud
from sgsa.reporte import resumir


def s(id_, tipo, estado, responsable=None):
    sol = Solicitud.registrar(id_, NuevaSolicitud("10001", "A", "a@b.c", tipo, "descripcion larga", False), date(2026, 1, 1))
    sol.estado, sol.responsable = estado, responsable
    return sol


def test_resumen_vacio():
    r = resumir([])
    assert r.total == 0 and r.porcentaje_resueltas is None
    assert formatear_resumen(r)[-1] == "Porcentaje resueltas: 0%"


def test_resumen_cuenta_solo_abiertas_en_alta_y_sin_responsable():
    r = resumir([
        s(1, TipoSolicitud.RECLAMO_DE_NOTA, Estado.PENDIENTE),                # alta, abierta, sin resp.
        s(2, TipoSolicitud.RECLAMO_DE_NOTA, Estado.RESUELTA, "Bedelia"),      # alta pero cerrada
        s(3, TipoSolicitud.BAJA_DE_MATERIA, Estado.RECHAZADA),                # cerrada sin resp.
    ])
    assert r.total == 3
    assert r.por_estado[Estado.PENDIENTE] == 1 and r.por_estado[Estado.RESUELTA] == 1
    assert r.abiertas_prioridad_alta == 1
    assert r.abiertas_sin_responsable == 1
    assert r.porcentaje_resueltas == 33.3
