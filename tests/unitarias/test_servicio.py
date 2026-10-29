from datetime import date

import pytest

from sgsa.busqueda import CriterioBusqueda
from sgsa.dominio import Estado, Prioridad, TipoSolicitud
from sgsa.dto import NuevaSolicitud
from sgsa.errores import DatoInvalido, SolicitudCerrada, SolicitudNoEncontrada, TransicionInvalida
from sgsa.repositorio import RepositorioEnMemoria
from sgsa.servicio import ServicioSolicitudes


@pytest.fixture
def servicio():
    # Repositorio en memoria y fecha fija: la prueba no toca disco ni depende del dia.
    return ServicioSolicitudes(RepositorioEnMemoria(), hoy=lambda: date(2026, 10, 29))


def datos(legajo="10001", tipo=TipoSolicitud.RECLAMO_DE_NOTA, urgente=False, descripcion="Reclamo de nota del parcial"):
    return NuevaSolicitud(legajo, "Ana Gomez", "ana@example.com", tipo, descripcion, urgente)


def test_registrar_asigna_id_fecha_y_prioridad(servicio):
    s = servicio.registrar(datos(tipo=TipoSolicitud.CERTIFICADO_ALUMNO_REGULAR, urgente=True))
    assert (s.id, s.fecha, s.prioridad, s.estado) == (1, "2026-10-29", Prioridad.MEDIA, Estado.PENDIENTE)
    assert servicio.buscar_estudiante("10001").email == "ana@example.com"


def test_registrar_valida_aunque_no_pase_por_la_consola(servicio):
    with pytest.raises(DatoInvalido):
        servicio.registrar(datos(descripcion="corta"))
    assert servicio.listar() == []


def test_cambiar_estado(servicio):
    servicio.registrar(datos())
    assert servicio.cambiar_estado(1, Estado.EN_PROCESO).estado is Estado.EN_PROCESO
    with pytest.raises(TransicionInvalida):
        servicio.cambiar_estado(1, Estado.PENDIENTE)


def test_solicitud_inexistente(servicio):
    with pytest.raises(SolicitudNoEncontrada, match="no existe la solicitud 5"):
        servicio.cambiar_estado(5, Estado.EN_PROCESO)


def test_asignar_responsable(servicio):
    servicio.registrar(datos())
    s = servicio.asignar_responsable(1, "Tesoreria")
    assert (s.responsable, s.estado) == ("Tesoreria", Estado.EN_PROCESO)


def test_asignar_responsable_fuera_del_catalogo(servicio):
    servicio.registrar(datos())
    with pytest.raises(DatoInvalido, match="responsable invalido"):
        servicio.asignar_responsable(1, "Rectorado")


def test_obtener_asignable_rechaza_cerradas(servicio):
    servicio.registrar(datos())
    servicio.cambiar_estado(1, Estado.RECHAZADA)
    with pytest.raises(SolicitudCerrada):
        servicio.obtener_asignable(1)


def test_catalogo_de_responsables_inyectable():
    # Antes un quinto responsable quedaba inaccesible por el numero magico 4 (S10).
    areas = ("A1", "A2", "A3", "A4", "A5")
    servicio = ServicioSolicitudes(RepositorioEnMemoria(), responsables=areas)
    servicio.registrar(datos())
    assert servicio.asignar_responsable(1, "A5").responsable == "A5"


@pytest.mark.parametrize("criterio, valor, ids", [
    (CriterioBusqueda.LEGAJO, "10001", [1, 3]),
    (CriterioBusqueda.ESTADO, "p", [1, 2, 3]),
    (CriterioBusqueda.TIPO, "1", [2]),
    (CriterioBusqueda.PRIORIDAD, "3", [1]),
    (CriterioBusqueda.PRIORIDAD, "ALTA", []),
])
def test_buscar(servicio, criterio, valor, ids):
    servicio.registrar(datos("10001", TipoSolicitud.RECLAMO_DE_NOTA))
    servicio.registrar(datos("10002", TipoSolicitud.CERTIFICADO_ALUMNO_REGULAR))
    servicio.registrar(datos("10001", TipoSolicitud.BAJA_DE_MATERIA))
    assert [s.id for s in servicio.buscar(criterio, valor)] == ids
