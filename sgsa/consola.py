"""Interfaz de consola: unica capa que lee del teclado y escribe en pantalla.

Traduce lo que escribe el usuario en llamadas al servicio y muestra los
errores de negocio (ErrorSGSA) con el formato "Error: <mensaje>".
`entrada` y `salida` se inyectan para poder probar la consola sin teclado.
"""
from sgsa.busqueda import CriterioBusqueda
from sgsa.dominio import Estado, TipoSolicitud
from sgsa.dto import NuevaSolicitud
from sgsa.errores import DatoInvalido, ErrorSGSA
from sgsa.formato import formatear_opciones, formatear_resumen, formatear_solicitud
from sgsa.validaciones import ValidadorSolicitud

OPCION_SALIR = "0"


class ConsolaSolicitudes:

    def __init__(self, servicio, validador=None, entrada=input, salida=print):
        self._servicio = servicio
        self._validador = validador or ValidadorSolicitud()
        self._entrada = entrada
        self._salida = salida
        self._opciones = {
            "1": ("Registrar solicitud", self.registrar_solicitud),
            "2": ("Cambiar estado", self.cambiar_estado),
            "3": ("Asignar responsable", self.asignar_responsable),
            "4": ("Buscar solicitudes", self.buscar),
            "5": ("Listar todas", self.listar),
            "6": ("Reporte", self.reporte),
        }

    # --- Bucle principal -------------------------------------------------

    def ejecutar(self):
        while True:
            self._mostrar_menu()
            opcion = self._entrada("Opcion: ")
            if opcion == OPCION_SALIR:
                self._salida("Hasta luego")
                return
            accion = self._opciones.get(opcion)
            if accion is None:
                self._salida("Opcion invalida")
                continue
            _, ejecutar_opcion = accion
            try:
                ejecutar_opcion()
            except ErrorSGSA as error:
                self._salida(f"Error: {error}")

    def _mostrar_menu(self):
        self._salida("")
        self._salida("===== SISTEMA DE SOLICITUDES ACADEMICAS =====")
        for codigo, (titulo, _) in self._opciones.items():
            self._salida(f"{codigo}. {titulo}")
        self._salida(f"{OPCION_SALIR}. Salir")

    # --- Casos de uso ------------------------------------------------------

    def registrar_solicitud(self):
        self._salida("--- Nueva solicitud ---")
        legajo = self._leer("Legajo: ")
        self._validador.validar_legajo(legajo)
        nombre, email = self._datos_del_estudiante(legajo)
        self._salida("Tipos: " + formatear_opciones((t.codigo, t.etiqueta) for t in TipoSolicitud))
        tipo = self._validador.validar_tipo(self._leer("Tipo: "))
        descripcion = self._leer("Descripcion: ")
        self._validador.validar_descripcion(descripcion)
        urgente = self._leer("Es urgente? (s/n): ").lower() == "s"
        nueva = NuevaSolicitud(legajo, nombre, email, tipo, descripcion, urgente)
        solicitud = self._servicio.registrar(nueva)
        self._salida(f"Solicitud registrada con ID {solicitud.id}")

    def cambiar_estado(self):
        self._salida("--- Cambiar estado ---")
        solicitud = self._servicio.obtener(self._leer_id())
        self._salida(f"Estado actual: {solicitud.estado.etiqueta}")
        self._salida("Nuevo estado: " + formatear_opciones((e.codigo, e.etiqueta) for e in Estado))
        nuevo_estado = Estado.desde_codigo(self._leer("Estado: ").upper())
        if nuevo_estado is None:
            raise DatoInvalido("estado invalido")
        self._servicio.cambiar_estado(solicitud.id, nuevo_estado)
        self._salida(f"Estado actualizado a {nuevo_estado.etiqueta}")

    def asignar_responsable(self):
        self._salida("--- Asignar responsable ---")
        solicitud = self._servicio.obtener_asignable(self._leer_id())
        responsables = self._servicio.responsables
        for numero, responsable in enumerate(responsables, start=1):
            self._salida(f"{numero}. {responsable}")
        numero = self._leer_entero("Responsable: ")
        if numero is None or not 1 <= numero <= len(responsables):
            raise DatoInvalido("responsable invalido")
        responsable = responsables[numero - 1]
        self._servicio.asignar_responsable(solicitud.id, responsable)
        self._salida(f"Solicitud {solicitud.id} asignada a {responsable}")

    def buscar(self):
        self._salida("--- Buscar ---")
        self._salida(" ".join(f"{c.codigo}. Por {c.etiqueta}" for c in CriterioBusqueda))
        criterio = CriterioBusqueda.desde_codigo(self._leer("Criterio: "))
        valor = self._leer("Valor: ")
        if criterio is None:
            raise DatoInvalido("criterio invalido")
        encontradas = self._servicio.buscar(criterio, valor)
        if not encontradas:
            self._salida("No se encontraron solicitudes")
        for solicitud in encontradas:
            self._salida(formatear_solicitud(solicitud))

    def listar(self):
        self._salida("--- Todas las solicitudes ---")
        solicitudes = self._servicio.listar()
        if not solicitudes:
            self._salida("No hay solicitudes cargadas")
        for solicitud in solicitudes:
            self._salida(formatear_solicitud(solicitud))

    def reporte(self):
        self._salida("--- Reporte ---")
        for linea in formatear_resumen(self._servicio.resumen()):
            self._salida(linea)

    # --- Lectura de datos ---------------------------------------------------

    def _datos_del_estudiante(self, legajo):
        estudiante = self._servicio.buscar_estudiante(legajo)
        if estudiante is not None:
            self._salida(f"Estudiante encontrado: {estudiante.nombre}")
            return estudiante.nombre, estudiante.email
        nombre = self._leer("Nombre y apellido: ")
        self._validador.validar_nombre(nombre)
        email = self._leer("Email: ")
        self._validador.validar_email(email)
        return nombre, email

    def _leer(self, mensaje):
        return self._entrada(mensaje).strip()

    def _leer_entero(self, mensaje):
        try:
            return int(self._entrada(mensaje))
        except ValueError:
            return None

    def _leer_id(self):
        id_solicitud = self._leer_entero("ID de la solicitud: ")
        if id_solicitud is None:
            raise DatoInvalido("el ID debe ser un numero")
        return id_solicitud
