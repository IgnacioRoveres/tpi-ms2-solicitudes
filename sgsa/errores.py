"""Errores del sistema. El mensaje de cada error es el texto que ve el usuario."""


class ErrorSGSA(Exception):
    """Base de todos los errores de negocio del sistema."""


class DatoInvalido(ErrorSGSA):
    """Un dato ingresado no cumple las reglas de validacion."""


class SolicitudNoEncontrada(ErrorSGSA):
    def __init__(self, id_solicitud):
        super().__init__(f"no existe la solicitud {id_solicitud}")
        self.id_solicitud = id_solicitud


class TransicionInvalida(ErrorSGSA):
    def __init__(self, actual, nuevo):
        super().__init__(f"no se puede pasar de {actual.etiqueta} a {nuevo.etiqueta}")


class SolicitudCerrada(ErrorSGSA):
    def __init__(self):
        super().__init__("la solicitud esta cerrada")


class DatosCorruptos(ErrorSGSA):
    """El archivo de datos existe pero no se puede leer."""
