"""Entidades del dominio con su comportamiento.

En la version inicial las solicitudes eran diccionarios y las reglas
(cambiar estado, asignar) estaban en la clase de interfaz. Ahora cada regla
vive en la entidad a la que pertenece.
"""
from dataclasses import dataclass
from typing import Optional

from sgsa.dominio import Estado, Prioridad, TipoSolicitud
from sgsa.errores import SolicitudCerrada, TransicionInvalida

# Catalogo de areas que pueden atender solicitudes.
AREAS_RESPONSABLES = ("Bedelia", "Secretaria Academica", "Tesoreria", "Coordinacion de Carrera")


@dataclass
class Estudiante:
    legajo: str
    nombre: str
    email: str


@dataclass
class Solicitud:
    id: int
    legajo: str
    tipo: TipoSolicitud
    descripcion: str
    urgente: bool
    prioridad: Prioridad
    fecha: str
    estado: Estado = Estado.PENDIENTE
    responsable: Optional[str] = None

    @classmethod
    def registrar(cls, id_solicitud, nueva, fecha):
        """Crea una solicitud pendiente a partir de los datos ingresados."""
        return cls(
            id=id_solicitud,
            legajo=nueva.legajo,
            tipo=nueva.tipo,
            descripcion=nueva.descripcion,
            urgente=nueva.urgente,
            prioridad=nueva.prioridad,
            fecha=fecha.isoformat(),
        )

    @property
    def esta_abierta(self):
        return self.estado.esta_abierto

    def verificar_abierta(self):
        if not self.esta_abierta:
            raise SolicitudCerrada()

    def cambiar_estado(self, nuevo_estado):
        if not self.estado.puede_pasar_a(nuevo_estado):
            raise TransicionInvalida(self.estado, nuevo_estado)
        self.estado = nuevo_estado

    def asignar_a(self, responsable):
        """Asigna un area. Una solicitud pendiente pasa a estar en proceso."""
        self.verificar_abierta()
        self.responsable = responsable
        if self.estado is Estado.PENDIENTE:
            self.estado = Estado.EN_PROCESO
