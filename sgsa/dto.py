"""Objetos de parametro (Introduce Parameter Object).

Agrupan datos que siempre viajan juntos y reemplazan listas largas de
parametros posicionales.
"""
from dataclasses import dataclass

from sgsa.dominio import TipoSolicitud


@dataclass(frozen=True)
class NuevaSolicitud:
    """Datos que ingresa el usuario para dar de alta una solicitud."""
    legajo: str
    nombre: str
    email: str
    tipo: TipoSolicitud
    descripcion: str
    urgente: bool

    @property
    def prioridad(self):
        return self.tipo.prioridad_para(self.urgente)
