"""Reglas de validacion de los datos de una solicitud.

Cada metodo lanza DatoInvalido con el mensaje que se muestra al usuario.
Se validan por separado porque la consola pide y valida campo por campo.
"""
from sgsa.dominio import TipoSolicitud
from sgsa.errores import DatoInvalido

LARGO_LEGAJO = 5
LARGO_MINIMO_DESCRIPCION = 10


class ValidadorSolicitud:

    def validar_legajo(self, legajo):
        if not (legajo.isdigit() and len(legajo) == LARGO_LEGAJO):
            raise DatoInvalido(f"el legajo debe tener {LARGO_LEGAJO} digitos")

    def validar_nombre(self, nombre):
        if not nombre:
            raise DatoInvalido("el nombre es obligatorio")

    def validar_email(self, email):
        if "@" not in email or "." not in email:
            raise DatoInvalido("email invalido")

    def validar_tipo(self, codigo_tipo):
        tipo = TipoSolicitud.desde_codigo(codigo_tipo)
        if tipo is None:
            raise DatoInvalido("tipo invalido")
        return tipo

    def validar_descripcion(self, descripcion):
        if len(descripcion) < LARGO_MINIMO_DESCRIPCION:
            raise DatoInvalido(
                f"la descripcion debe tener al menos {LARGO_MINIMO_DESCRIPCION} caracteres"
            )
