import pytest

from sgsa.dominio import TipoSolicitud
from sgsa.errores import DatoInvalido
from sgsa.validaciones import ValidadorSolicitud

v = ValidadorSolicitud()


@pytest.mark.parametrize("legajo", ["12345", "00001"])
def test_legajo_valido(legajo):
    v.validar_legajo(legajo)


@pytest.mark.parametrize("legajo", ["", "1234", "123456", "12a45", " 1234"])
def test_legajo_invalido(legajo):
    with pytest.raises(DatoInvalido, match="5 digitos"):
        v.validar_legajo(legajo)


@pytest.mark.parametrize("email", ["sinarroba.com", "a@sinpunto", ""])
def test_email_invalido(email):
    with pytest.raises(DatoInvalido, match="email invalido"):
        v.validar_email(email)


def test_nombre_obligatorio():
    with pytest.raises(DatoInvalido, match="obligatorio"):
        v.validar_nombre("")


def test_descripcion_en_el_limite():
    v.validar_descripcion("x" * 10)
    with pytest.raises(DatoInvalido, match="al menos 10"):
        v.validar_descripcion("x" * 9)


def test_tipo_valido_devuelve_el_enum_e_invalido_falla():
    assert v.validar_tipo("2") is TipoSolicitud.RECLAMO_DE_NOTA
    with pytest.raises(DatoInvalido, match="tipo invalido"):
        v.validar_tipo("6")
