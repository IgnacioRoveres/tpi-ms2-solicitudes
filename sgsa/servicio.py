"""Casos de uso del sistema.

No conoce la consola (no hace print ni input) ni el archivo: recibe el
repositorio por constructor (inyeccion de dependencias). Por eso se puede
probar con un repositorio en memoria y reutilizar desde otra interfaz.
"""
from datetime import date

from sgsa.errores import DatoInvalido, SolicitudNoEncontrada
from sgsa.modelos import AREAS_RESPONSABLES, Estudiante, Solicitud
from sgsa.reporte import resumir
from sgsa.validaciones import ValidadorSolicitud


class ServicioSolicitudes:

    def __init__(self, repositorio, validador=None, hoy=date.today, responsables=AREAS_RESPONSABLES):
        self._repositorio = repositorio
        self._validador = validador or ValidadorSolicitud()
        self._hoy = hoy
        self._responsables = tuple(responsables)

    @property
    def responsables(self):
        return self._responsables

    def buscar_estudiante(self, legajo):
        return self._repositorio.obtener_estudiante(legajo)

    def registrar(self, nueva):
        self._validar(nueva)
        solicitud = Solicitud.registrar(self._repositorio.reservar_id(), nueva, self._hoy())
        estudiante = Estudiante(nueva.legajo, nueva.nombre, nueva.email)
        self._repositorio.agregar(solicitud, estudiante)
        return solicitud

    def obtener(self, id_solicitud):
        solicitud = self._repositorio.obtener(id_solicitud)
        if solicitud is None:
            raise SolicitudNoEncontrada(id_solicitud)
        return solicitud

    def obtener_asignable(self, id_solicitud):
        solicitud = self.obtener(id_solicitud)
        solicitud.verificar_abierta()
        return solicitud

    def cambiar_estado(self, id_solicitud, nuevo_estado):
        solicitud = self.obtener(id_solicitud)
        solicitud.cambiar_estado(nuevo_estado)
        self._repositorio.actualizar(solicitud)
        return solicitud

    def asignar_responsable(self, id_solicitud, responsable):
        if responsable not in self._responsables:
            raise DatoInvalido("responsable invalido")
        solicitud = self.obtener(id_solicitud)
        solicitud.asignar_a(responsable)
        self._repositorio.actualizar(solicitud)
        return solicitud

    def listar(self):
        return self._repositorio.listar()

    def buscar(self, criterio, valor):
        return [s for s in self._repositorio.listar() if criterio.coincide(s, valor)]

    def resumen(self):
        return resumir(self._repositorio.listar())

    def _validar(self, nueva):
        self._validador.validar_legajo(nueva.legajo)
        self._validador.validar_nombre(nueva.nombre)
        self._validador.validar_email(nueva.email)
        self._validador.validar_descripcion(nueva.descripcion)
