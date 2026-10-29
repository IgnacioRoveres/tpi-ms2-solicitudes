"""Casos de uso del sistema.

No conoce la consola (no hace print ni input) ni el archivo: recibe el
repositorio por constructor (inyeccion de dependencias). Por eso se puede
probar con un repositorio en memoria y reutilizar desde otra interfaz.
"""
from datetime import date
from typing import Callable, Iterable

from sgsa.busqueda import CriterioBusqueda
from sgsa.dominio import Estado
from sgsa.dto import NuevaSolicitud
from sgsa.errores import DatoInvalido, SolicitudNoEncontrada
from sgsa.modelos import AREAS_RESPONSABLES, Estudiante, Solicitud
from sgsa.reporte import ResumenSolicitudes, resumir
from sgsa.repositorio import RepositorioSolicitudes
from sgsa.validaciones import ValidadorSolicitud


class ServicioSolicitudes:

    def __init__(
        self,
        repositorio: RepositorioSolicitudes,
        validador: ValidadorSolicitud | None = None,
        hoy: Callable[[], date] = date.today,
        responsables: Iterable[str] = AREAS_RESPONSABLES,
    ):
        self._repositorio = repositorio
        self._validador = validador or ValidadorSolicitud()
        self._hoy = hoy
        self._responsables = tuple(responsables)

    @property
    def responsables(self) -> tuple[str, ...]:
        return self._responsables

    def buscar_estudiante(self, legajo: str) -> Estudiante | None:
        return self._repositorio.obtener_estudiante(legajo)

    def registrar(self, nueva: NuevaSolicitud) -> Solicitud:
        self._validar(nueva)
        solicitud = Solicitud.registrar(self._repositorio.reservar_id(), nueva, self._hoy())
        estudiante = Estudiante(nueva.legajo, nueva.nombre, nueva.email)
        self._repositorio.agregar(solicitud, estudiante)
        return solicitud

    def obtener(self, id_solicitud: int) -> Solicitud:
        solicitud = self._repositorio.obtener(id_solicitud)
        if solicitud is None:
            raise SolicitudNoEncontrada(id_solicitud)
        return solicitud

    def obtener_asignable(self, id_solicitud: int) -> Solicitud:
        solicitud = self.obtener(id_solicitud)
        solicitud.verificar_abierta()
        return solicitud

    def cambiar_estado(self, id_solicitud: int, nuevo_estado: Estado) -> Solicitud:
        solicitud = self.obtener(id_solicitud)
        solicitud.cambiar_estado(nuevo_estado)
        self._repositorio.actualizar(solicitud)
        return solicitud

    def asignar_responsable(self, id_solicitud: int, responsable: str) -> Solicitud:
        if responsable not in self._responsables:
            raise DatoInvalido("responsable invalido")
        solicitud = self.obtener(id_solicitud)
        solicitud.asignar_a(responsable)
        self._repositorio.actualizar(solicitud)
        return solicitud

    def listar(self) -> list[Solicitud]:
        return self._repositorio.listar()

    def buscar(self, criterio: CriterioBusqueda, valor: str) -> list[Solicitud]:
        return [s for s in self._repositorio.listar() if criterio.coincide(s, valor)]

    def resumen(self) -> ResumenSolicitudes:
        return resumir(self._repositorio.listar())

    def _validar(self, nueva: NuevaSolicitud) -> None:
        self._validador.validar_legajo(nueva.legajo)
        self._validador.validar_nombre(nueva.nombre)
        self._validador.validar_email(nueva.email)
        self._validador.validar_descripcion(nueva.descripcion)
