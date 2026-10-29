"""Persistencia de solicitudes (inversion de dependencias).

El servicio depende de la abstraccion RepositorioSolicitudes, no de un
archivo concreto. Hay dos implementaciones intercambiables (LSP):
RepositorioJSON, la del programa, y RepositorioEnMemoria, para pruebas.
"""
import json
from abc import ABC, abstractmethod

from sgsa.dominio import Estado, Prioridad, TipoSolicitud
from sgsa.errores import DatosCorruptos
from sgsa.modelos import Estudiante, Solicitud


class RepositorioSolicitudes(ABC):

    @abstractmethod
    def reservar_id(self):
        """Devuelve el proximo ID libre y lo marca como usado."""

    @abstractmethod
    def agregar(self, solicitud, estudiante):
        """Guarda una solicitud nueva junto con los datos de su estudiante."""

    @abstractmethod
    def actualizar(self, solicitud):
        """Persiste los cambios de una solicitud existente."""

    @abstractmethod
    def obtener(self, id_solicitud):
        """Devuelve la solicitud o None si no existe."""

    @abstractmethod
    def listar(self):
        """Devuelve todas las solicitudes en orden de alta."""

    @abstractmethod
    def obtener_estudiante(self, legajo):
        """Devuelve el estudiante o None si no esta registrado."""


class RepositorioEnMemoria(RepositorioSolicitudes):

    def __init__(self):
        self._estudiantes = {}
        self._solicitudes = []
        self._ultimo_id = 0

    def reservar_id(self):
        self._ultimo_id += 1
        return self._ultimo_id

    def agregar(self, solicitud, estudiante):
        self._estudiantes[estudiante.legajo] = estudiante
        self._solicitudes.append(solicitud)
        self._al_modificar()

    def actualizar(self, solicitud):
        self._al_modificar()

    def obtener(self, id_solicitud):
        return next((s for s in self._solicitudes if s.id == id_solicitud), None)

    def listar(self):
        return list(self._solicitudes)

    def obtener_estudiante(self, legajo):
        return self._estudiantes.get(legajo)

    def _al_modificar(self):
        """Gancho para subclases que necesitan persistir (Template Method)."""


class RepositorioJSON(RepositorioEnMemoria):
    """Mantiene los datos en memoria y los vuelca a un archivo en cada cambio.

    El formato del archivo es el mismo de la version inicial.
    """

    def __init__(self, ruta):
        super().__init__()
        self._ruta = ruta
        if ruta.exists():
            self._cargar()

    def _cargar(self):
        try:
            datos = json.loads(self._ruta.read_text(encoding="utf-8"))
            self._estudiantes = {
                legajo: Estudiante(**e) for legajo, e in datos["estudiantes"].items()
            }
            self._solicitudes = [_solicitud_desde_dict(s) for s in datos["solicitudes"]]
            self._ultimo_id = datos["ultimo_id"]
        except (ValueError, KeyError, TypeError) as error:
            raise DatosCorruptos(
                f"el archivo {self._ruta.name} esta danado y no se modifico. "
                "Reviselo o eliminelo para empezar de cero."
            ) from error

    def _al_modificar(self):
        datos = {
            "estudiantes": {
                legajo: {"legajo": e.legajo, "nombre": e.nombre, "email": e.email}
                for legajo, e in self._estudiantes.items()
            },
            "solicitudes": [_solicitud_a_dict(s) for s in self._solicitudes],
            "ultimo_id": self._ultimo_id,
        }
        self._ruta.write_text(json.dumps(datos, indent=2, ensure_ascii=False), encoding="utf-8")


def _solicitud_a_dict(solicitud):
    return {
        "id": solicitud.id,
        "legajo": solicitud.legajo,
        "tipo": solicitud.tipo.codigo,
        "descripcion": solicitud.descripcion,
        "urgente": solicitud.urgente,
        "prioridad": int(solicitud.prioridad),
        "estado": solicitud.estado.codigo,
        "responsable": solicitud.responsable,
        "fecha": solicitud.fecha,
    }


def _solicitud_desde_dict(datos):
    tipo = TipoSolicitud.desde_codigo(datos["tipo"])
    estado = Estado.desde_codigo(datos["estado"])
    if tipo is None or estado is None:
        raise ValueError(f"codigo desconocido en la solicitud {datos['id']}")
    return Solicitud(
        id=datos["id"],
        legajo=datos["legajo"],
        tipo=tipo,
        descripcion=datos["descripcion"],
        urgente=datos["urgente"],
        prioridad=Prioridad(datos["prioridad"]),
        fecha=datos["fecha"],
        estado=estado,
        responsable=datos["responsable"],
    )
