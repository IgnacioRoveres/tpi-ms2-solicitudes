# Sistema de Gestion de Solicitudes Academicas
# version 1.0 - hecho rapido para la demo
import json
import os
import sys
from datetime import date

from sgsa.dominio import Estado, Prioridad, TipoSolicitud
from sgsa.errores import DatoInvalido
from sgsa.validaciones import ValidadorSolicitud

ARCHIVO = "solicitudes.json"

# responsables disponibles
RESPONSABLES = ["Bedelia", "Secretaria Academica", "Tesoreria", "Coordinacion de Carrera"]

datos = {"estudiantes": {}, "solicitudes": [], "ultimo_id": 0}


class Sistema:

    def __init__(self):
        self.d = datos
        self.validador = ValidadorSolicitud()
        self.cargar()

    def cargar(self):
        if not os.path.exists(ARCHIVO):
            return
        try:
            with open(ARCHIVO, "r", encoding="utf-8") as f:
                self.d = json.load(f)
        except (json.JSONDecodeError, UnicodeDecodeError):
            print("Error: el archivo " + ARCHIVO + " esta danado y no se modifico. Reviselo o eliminelo para empezar de cero.")
            sys.exit(1)

    def guardar(self):
        f = open(ARCHIVO, "w", encoding="utf-8")
        json.dump(self.d, f, indent=2, ensure_ascii=False)
        f.close()

    def menu(self):
        while True:
            print("")
            print("===== SISTEMA DE SOLICITUDES ACADEMICAS =====")
            print("1. Registrar solicitud")
            print("2. Cambiar estado")
            print("3. Asignar responsable")
            print("4. Buscar solicitudes")
            print("5. Listar todas")
            print("6. Reporte")
            print("0. Salir")
            op = input("Opcion: ")
            if op == "1":
                self.registrar_solicitud()
            elif op == "2":
                self.cambiar_estado()
            elif op == "3":
                self.asignar()
            elif op == "4":
                self.buscar()
            elif op == "5":
                self.listar()
            elif op == "6":
                self.reporte()
            elif op == "0":
                print("Hasta luego")
                break
            else:
                print("Opcion invalida")

    def registrar_solicitud(self):
        print("--- Nueva solicitud ---")
        try:
            legajo = input("Legajo: ").strip()
            self.validador.validar_legajo(legajo)
            estudiante = self.obtener_o_pedir_estudiante(legajo)
            print("Tipos: " + " ".join(tipo.codigo + "-" + tipo.etiqueta for tipo in TipoSolicitud))
            tipo = self.validador.validar_tipo(input("Tipo: ").strip())
            desc = input("Descripcion: ").strip()
            self.validador.validar_descripcion(desc)
        except DatoInvalido as error:
            print("Error: " + str(error))
            return
        urgente = input("Es urgente? (s/n): ").strip().lower() == "s"
        p = tipo.prioridad_para(urgente)
        self.crear_solicitud(legajo, estudiante["nombre"], estudiante["email"], tipo.codigo, desc, urgente, int(p), str(date.today()))

    def obtener_o_pedir_estudiante(self, legajo):
        """Devuelve el estudiante registrado o pide sus datos (lanza DatoInvalido)."""
        if legajo in self.d["estudiantes"]:
            estudiante = self.d["estudiantes"][legajo]
            print("Estudiante encontrado: " + estudiante["nombre"])
            return estudiante
        nombre = input("Nombre y apellido: ").strip()
        self.validador.validar_nombre(nombre)
        email = input("Email: ").strip()
        self.validador.validar_email(email)
        return {"legajo": legajo, "nombre": nombre, "email": email}

    def crear_solicitud(self, legajo, nombre, email, t, desc, urgente, p, fecha):
        self.d["estudiantes"][legajo] = {"legajo": legajo, "nombre": nombre, "email": email}
        self.d["ultimo_id"] = self.d["ultimo_id"] + 1
        s = {}
        s["id"] = self.d["ultimo_id"]
        s["legajo"] = legajo
        s["tipo"] = t
        s["descripcion"] = desc
        s["urgente"] = urgente
        s["prioridad"] = p
        s["estado"] = Estado.PENDIENTE.codigo
        s["responsable"] = None
        s["fecha"] = fecha
        self.d["solicitudes"].append(s)
        self.guardar()
        print("Solicitud registrada con ID " + str(s["id"]))

    def cambiar_estado(self):
        print("--- Cambiar estado ---")
        sol = self.pedir_solicitud()
        if sol == None:
            return
        actual = Estado.desde_codigo(sol["estado"])
        print("Estado actual: " + actual.etiqueta)
        print("Nuevo estado: " + " ".join(e.codigo + "-" + e.etiqueta for e in Estado))
        nuevo = Estado.desde_codigo(input("Estado: ").strip().upper())
        if nuevo == None:
            print("Error: estado invalido")
            return
        if not actual.puede_pasar_a(nuevo):
            print("Error: no se puede pasar de " + actual.etiqueta + " a " + nuevo.etiqueta)
            return
        sol["estado"] = nuevo.codigo
        self.guardar()
        print("Estado actualizado a " + nuevo.etiqueta)

    def asignar(self):
        print("--- Asignar responsable ---")
        sol = self.pedir_solicitud()
        if sol == None:
            return
        if not self.esta_abierta(sol):
            print("Error: la solicitud esta cerrada")
            return
        i = 1
        for r in RESPONSABLES:
            print(str(i) + ". " + r)
            i = i + 1
        n = self.pedir_numero("Responsable: ")
        if n == None or n < 1 or n > 4:
            print("Error: responsable invalido")
            return
        sol["responsable"] = RESPONSABLES[n - 1]
        if sol["estado"] == Estado.PENDIENTE.codigo:
            sol["estado"] = Estado.EN_PROCESO.codigo
        self.guardar()
        print("Solicitud " + str(sol["id"]) + " asignada a " + RESPONSABLES[n - 1])

    def buscar(self):
        print("--- Buscar ---")
        print("1. Por legajo 2. Por estado 3. Por tipo 4. Por prioridad")
        c = input("Criterio: ").strip()
        v = input("Valor: ").strip()
        l = []
        if c == "1":
            for x in self.d["solicitudes"]:
                if x["legajo"] == v:
                    l.append(x)
        elif c == "2":
            for x in self.d["solicitudes"]:
                if x["estado"] == v.upper():
                    l.append(x)
        elif c == "3":
            for x in self.d["solicitudes"]:
                if x["tipo"] == v:
                    l.append(x)
        elif c == "4":
            for x in self.d["solicitudes"]:
                if str(x["prioridad"]) == v:
                    l.append(x)
        else:
            print("Error: criterio invalido")
            return
        if len(l) == 0:
            print("No se encontraron solicitudes")
            return
        for x in l:
            print(self.formatear_fila(x))

    def listar(self):
        print("--- Todas las solicitudes ---")
        if len(self.d["solicitudes"]) == 0:
            print("No hay solicitudes cargadas")
            return
        for x in self.d["solicitudes"]:
            print(self.formatear_fila(x))

    def formatear_fila(self, solicitud):
        tipo = TipoSolicitud.desde_codigo(solicitud["tipo"]).etiqueta
        prioridad = Prioridad(solicitud["prioridad"]).etiqueta
        estado = self.nombre_estado(solicitud["estado"])
        responsable = solicitud["responsable"] or "Sin asignar"
        return " | ".join(["#" + str(solicitud["id"]), solicitud["legajo"], tipo, prioridad, estado, responsable])

    def reporte(self):
        print("--- Reporte ---")
        total = len(self.d["solicitudes"])
        print("Total de solicitudes: " + str(total))
        cantidad = {}
        for estado in Estado:
            cantidad[estado] = 0
        for s in self.d["solicitudes"]:
            cantidad[Estado.desde_codigo(s["estado"])] += 1
        print("Pendientes: " + str(cantidad[Estado.PENDIENTE]))
        print("En proceso: " + str(cantidad[Estado.EN_PROCESO]))
        print("Resueltas: " + str(cantidad[Estado.RESUELTA]))
        print("Rechazadas: " + str(cantidad[Estado.RECHAZADA]))
        r = cantidad[Estado.RESUELTA]
        alta = 0
        for s in self.d["solicitudes"]:
            if s["prioridad"] == Prioridad.ALTA and self.esta_abierta(s):
                alta = alta + 1
        print("Abiertas con prioridad ALTA: " + str(alta))
        sin = 0
        for s in self.d["solicitudes"]:
            if s["responsable"] == None and self.esta_abierta(s):
                sin = sin + 1
        print("Abiertas sin responsable: " + str(sin))
        # porcentaje resueltas
        if total > 0:
            print("Porcentaje resueltas: " + str(round(r * 100 / total, 1)) + "%")
        else:
            print("Porcentaje resueltas: 0%")

    def esta_abierta(self, solicitud):
        return Estado.desde_codigo(solicitud["estado"]).esta_abierto

    def buscar_por_id(self, id_solicitud):
        for solicitud in self.d["solicitudes"]:
            if solicitud["id"] == id_solicitud:
                return solicitud
        return None

    def pedir_solicitud(self):
        """Pide un ID por teclado y devuelve la solicitud, o None informando el error."""
        id_solicitud = self.pedir_numero("ID de la solicitud: ")
        if id_solicitud == None:
            print("Error: el ID debe ser un numero")
            return None
        solicitud = self.buscar_por_id(id_solicitud)
        if solicitud == None:
            print("Error: no existe la solicitud " + str(id_solicitud))
        return solicitud

    def pedir_numero(self, mensaje):
        try:
            return int(input(mensaje))
        except ValueError:
            return None

    def nombre_estado(self, e):
        return Estado.desde_codigo(e).etiqueta

    # def exportar_csv(self):
    #     f = open("export.csv", "w")
    #     for s in self.d["solicitudes"]:
    #         f.write(str(s["id"]) + "," + s["legajo"] + "\n")
    #     f.close()


if __name__ == "__main__":
    s = Sistema()
    s.menu()
