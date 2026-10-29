"""Conceptos del dominio: estados, prioridades y tipos de solicitud.

Reemplazan los codigos magicos de la version inicial ("P", "E", 3, "2"...).
Cada valor conserva su `codigo`, que es lo que se guarda en el archivo JSON,
para que los datos sigan siendo compatibles.
"""
from enum import Enum, IntEnum


class Estado(Enum):
    PENDIENTE = ("P", "Pendiente")
    EN_PROCESO = ("E", "En proceso")
    RESUELTA = ("R", "Resuelta")
    RECHAZADA = ("X", "Rechazada")

    def __init__(self, codigo, etiqueta):
        self.codigo = codigo
        self.etiqueta = etiqueta

    @classmethod
    def desde_codigo(cls, codigo):
        for estado in cls:
            if estado.codigo == codigo:
                return estado
        return None

    @property
    def es_final(self):
        return not _TRANSICIONES_PERMITIDAS[self]

    def puede_pasar_a(self, nuevo_estado):
        return nuevo_estado in _TRANSICIONES_PERMITIDAS[self]


# Ciclo de vida: agregar un estado nuevo solo requiere tocar esta tabla.
_TRANSICIONES_PERMITIDAS = {
    Estado.PENDIENTE: {Estado.EN_PROCESO, Estado.RECHAZADA},
    Estado.EN_PROCESO: {Estado.RESUELTA, Estado.RECHAZADA},
    Estado.RESUELTA: set(),
    Estado.RECHAZADA: set(),
}


class Prioridad(IntEnum):
    BAJA = 1
    MEDIA = 2
    ALTA = 3

    @property
    def etiqueta(self):
        return self.name

    def elevada(self):
        """Sube un nivel, sin pasar de ALTA."""
        return Prioridad(min(self + 1, Prioridad.ALTA))


class TipoSolicitud(Enum):
    CERTIFICADO_ALUMNO_REGULAR = ("1", "Certificado de alumno regular", Prioridad.BAJA)
    RECLAMO_DE_NOTA = ("2", "Reclamo de nota", Prioridad.ALTA)
    EQUIVALENCIA_DE_MATERIAS = ("3", "Equivalencia de materias", Prioridad.MEDIA)
    EXCEPCION_DE_CORRELATIVIDAD = ("4", "Excepcion de correlatividad", Prioridad.MEDIA)
    BAJA_DE_MATERIA = ("5", "Baja de materia", Prioridad.MEDIA)

    def __init__(self, codigo, etiqueta, prioridad_base):
        self.codigo = codigo
        self.etiqueta = etiqueta
        self.prioridad_base = prioridad_base

    @classmethod
    def desde_codigo(cls, codigo):
        for tipo in cls:
            if tipo.codigo == codigo:
                return tipo
        return None
