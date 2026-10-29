from datetime import date

import pytest

from sgsa.dominio import Estado, Prioridad, TipoSolicitud
from sgsa.dto import NuevaSolicitud
from sgsa.errores import SolicitudCerrada, TransicionInvalida
from sgsa.modelos import Solicitud


def nueva(tipo=TipoSolicitud.RECLAMO_DE_NOTA, urgente=False):
    return NuevaSolicitud("10001", "Ana Gomez", "ana@example.com", tipo, "Reclamo de nota del parcial", urgente)


def solicitud(**cambios):
    s = Solicitud.registrar(1, nueva(), date(2026, 10, 29))
    for campo, valor in cambios.items():
        setattr(s, campo, valor)
    return s


@pytest.mark.parametrize("tipo, urgente, esperada", [
    (TipoSolicitud.CERTIFICADO_ALUMNO_REGULAR, False, Prioridad.BAJA),
    (TipoSolicitud.CERTIFICADO_ALUMNO_REGULAR, True, Prioridad.MEDIA),
    (TipoSolicitud.EQUIVALENCIA_DE_MATERIAS, False, Prioridad.MEDIA),
    (TipoSolicitud.EQUIVALENCIA_DE_MATERIAS, True, Prioridad.ALTA),
    (TipoSolicitud.RECLAMO_DE_NOTA, False, Prioridad.ALTA),
    (TipoSolicitud.RECLAMO_DE_NOTA, True, Prioridad.ALTA),  # tope en ALTA
])
def test_prioridad_segun_tipo_y_urgencia(tipo, urgente, esperada):
    assert tipo.prioridad_para(urgente) is esperada
    assert nueva(tipo, urgente).prioridad is esperada


def test_solicitud_registrada_arranca_pendiente_y_sin_responsable():
    s = Solicitud.registrar(7, nueva(), date(2026, 10, 29))
    assert (s.id, s.estado, s.responsable, s.fecha) == (7, Estado.PENDIENTE, None, "2026-10-29")


@pytest.mark.parametrize("desde, hacia", [
    (Estado.PENDIENTE, Estado.EN_PROCESO),
    (Estado.PENDIENTE, Estado.RECHAZADA),
    (Estado.EN_PROCESO, Estado.RESUELTA),
    (Estado.EN_PROCESO, Estado.RECHAZADA),
])
def test_transiciones_permitidas(desde, hacia):
    s = solicitud(estado=desde)
    s.cambiar_estado(hacia)
    assert s.estado is hacia


@pytest.mark.parametrize("desde, hacia", [
    (Estado.PENDIENTE, Estado.RESUELTA),
    (Estado.PENDIENTE, Estado.PENDIENTE),
    (Estado.EN_PROCESO, Estado.PENDIENTE),
    (Estado.RESUELTA, Estado.EN_PROCESO),
    (Estado.RECHAZADA, Estado.PENDIENTE),
])
def test_transiciones_prohibidas(desde, hacia):
    s = solicitud(estado=desde)
    with pytest.raises(TransicionInvalida, match=f"de {desde.etiqueta} a {hacia.etiqueta}"):
        s.cambiar_estado(hacia)
    assert s.estado is desde


def test_asignar_pendiente_la_pasa_a_en_proceso():
    s = solicitud()
    s.asignar_a("Bedelia")
    assert (s.responsable, s.estado) == ("Bedelia", Estado.EN_PROCESO)


def test_reasignar_en_proceso_mantiene_el_estado():
    s = solicitud(estado=Estado.EN_PROCESO, responsable="Bedelia")
    s.asignar_a("Tesoreria")
    assert (s.responsable, s.estado) == ("Tesoreria", Estado.EN_PROCESO)


@pytest.mark.parametrize("estado", [Estado.RESUELTA, Estado.RECHAZADA])
def test_no_se_asigna_una_solicitud_cerrada(estado):
    s = solicitud(estado=estado)
    with pytest.raises(SolicitudCerrada):
        s.asignar_a("Bedelia")
    assert s.responsable is None


def test_codigos_desconocidos_devuelven_none():
    assert Estado.desde_codigo("Z") is None
    assert TipoSolicitud.desde_codigo("9") is None
