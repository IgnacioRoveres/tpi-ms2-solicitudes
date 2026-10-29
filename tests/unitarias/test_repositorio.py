"""Contrato del repositorio: la MISMA prueba corre sobre las dos
implementaciones. Si ambas pasan, son intercambiables (LSP)."""
import json
from datetime import date

import pytest

from sgsa.dominio import Estado, TipoSolicitud
from sgsa.dto import NuevaSolicitud
from sgsa.errores import DatosCorruptos
from sgsa.modelos import Estudiante, Solicitud
from sgsa.repositorio import RepositorioEnMemoria, RepositorioJSON


@pytest.fixture(params=["memoria", "json"])
def repositorio(request, tmp_path):
    if request.param == "memoria":
        return RepositorioEnMemoria()
    return RepositorioJSON(tmp_path / "solicitudes.json")


def alta(repositorio, legajo="10001"):
    datos = NuevaSolicitud(legajo, "Ana Gomez", "ana@example.com", TipoSolicitud.BAJA_DE_MATERIA, "Baja de Programacion II", False)
    s = Solicitud.registrar(repositorio.reservar_id(), datos, date(2026, 10, 29))
    repositorio.agregar(s, Estudiante(legajo, "Ana Gomez", "ana@example.com"))
    return s


def test_ids_consecutivos(repositorio):
    assert [alta(repositorio).id for _ in range(3)] == [1, 2, 3]


def test_obtener_y_listar(repositorio):
    s = alta(repositorio)
    assert repositorio.obtener(s.id) == s
    assert repositorio.obtener(99) is None
    assert repositorio.listar() == [s]


def test_estudiante_guardado(repositorio):
    alta(repositorio)
    assert repositorio.obtener_estudiante("10001").nombre == "Ana Gomez"
    assert repositorio.obtener_estudiante("99999") is None


def test_json_persiste_entre_instancias(tmp_path):
    ruta = tmp_path / "solicitudes.json"
    repo = RepositorioJSON(ruta)
    s = alta(repo)
    s.cambiar_estado(Estado.EN_PROCESO)
    repo.actualizar(s)
    recargado = RepositorioJSON(ruta)
    assert recargado.obtener(1) == s
    assert recargado.reservar_id() == 2


def test_json_lee_archivos_de_la_version_inicial(tmp_path):
    ruta = tmp_path / "solicitudes.json"
    ruta.write_text(json.dumps({
        "estudiantes": {"10001": {"legajo": "10001", "nombre": "Ana Gomez", "email": "ana@example.com"}},
        "solicitudes": [{"id": 1, "legajo": "10001", "tipo": "2", "descripcion": "Reclamo de nota", "urgente": True,
                         "prioridad": 3, "estado": "E", "responsable": "Bedelia", "fecha": "2026-10-01"}],
        "ultimo_id": 1,
    }), encoding="utf-8")
    s = RepositorioJSON(ruta).obtener(1)
    assert (s.tipo, s.estado, s.responsable) == (TipoSolicitud.RECLAMO_DE_NOTA, Estado.EN_PROCESO, "Bedelia")


@pytest.mark.parametrize("contenido", ['{"estudiantes": ', '{"otra": 1}', '{"estudiantes": {}, "solicitudes": [{"id": 1, "tipo": "9"}], "ultimo_id": 1}'])
def test_json_danado_lanza_error_y_no_toca_el_archivo(tmp_path, contenido):
    ruta = tmp_path / "solicitudes.json"
    ruta.write_text(contenido, encoding="utf-8")
    with pytest.raises(DatosCorruptos):
        RepositorioJSON(ruta)
    assert ruta.read_text(encoding="utf-8") == contenido


def test_json_no_crea_archivo_si_no_hay_cambios(tmp_path):
    ruta = tmp_path / "solicitudes.json"
    RepositorioJSON(ruta).listar()
    assert not ruta.exists()
