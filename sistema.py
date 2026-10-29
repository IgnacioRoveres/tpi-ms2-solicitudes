# Sistema de Gestion de Solicitudes Academicas
# version 1.0 - hecho rapido para la demo
import json
import os
import sys
from datetime import date

ARCHIVO = "solicitudes.json"

# responsables disponibles
RESPONSABLES = ["Bedelia", "Secretaria Academica", "Tesoreria", "Coordinacion de Carrera"]

datos = {"estudiantes": {}, "solicitudes": [], "ultimo_id": 0}


class Sistema:

    def __init__(self):
        self.d = datos
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
        legajo = input("Legajo: ").strip()
        # validar legajo
        if not legajo.isdigit() or len(legajo) != 5:
            print("Error: el legajo debe tener 5 digitos")
            return
        if legajo in self.d["estudiantes"]:
            nombre = self.d["estudiantes"][legajo]["nombre"]
            email = self.d["estudiantes"][legajo]["email"]
            print("Estudiante encontrado: " + nombre)
        else:
            nombre = input("Nombre y apellido: ").strip()
            if nombre == "":
                print("Error: el nombre es obligatorio")
                return
            email = input("Email: ").strip()
            if "@" not in email or "." not in email:
                print("Error: email invalido")
                return
        print("Tipos: 1-Certificado de alumno regular 2-Reclamo de nota 3-Equivalencia de materias 4-Excepcion de correlatividad 5-Baja de materia")
        t = input("Tipo: ").strip()
        if t not in ["1", "2", "3", "4", "5"]:
            print("Error: tipo invalido")
            return
        desc = input("Descripcion: ").strip()
        if len(desc) < 10:
            print("Error: la descripcion debe tener al menos 10 caracteres")
            return
        urg = input("Es urgente? (s/n): ").strip().lower()
        # calcular prioridad
        if t == "2":
            p = 3
        elif t == "1":
            p = 1
        else:
            p = 2
        if urg == "s":
            p = p + 1
            if p > 3:
                p = 3
        self.crear_solicitud(legajo, nombre, email, t, desc, urg == "s", p, str(date.today()))

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
        s["estado"] = "P"
        s["responsable"] = None
        s["fecha"] = fecha
        self.d["solicitudes"].append(s)
        self.guardar()
        print("Solicitud registrada con ID " + str(s["id"]))

    def cambiar_estado(self):
        print("--- Cambiar estado ---")
        id = self.pedir_numero("ID de la solicitud: ")
        if id == None:
            print("Error: el ID debe ser un numero")
            return
        sol = None
        for x in self.d["solicitudes"]:
            if x["id"] == id:
                sol = x
        if sol == None:
            print("Error: no existe la solicitud " + str(id))
            return
        print("Estado actual: " + self.nombre_estado(sol["estado"]))
        print("Nuevo estado: P-Pendiente E-En proceso R-Resuelta X-Rechazada")
        nuevo = input("Estado: ").strip().upper()
        if nuevo not in ["P", "E", "R", "X"]:
            print("Error: estado invalido")
            return
        # reglas de transicion
        ok = False
        if sol["estado"] == "P" and (nuevo == "E" or nuevo == "X"):
            ok = True
        if sol["estado"] == "E" and (nuevo == "R" or nuevo == "X"):
            ok = True
        if ok == False:
            print("Error: no se puede pasar de " + self.nombre_estado(sol["estado"]) + " a " + self.nombre_estado(nuevo))
            return
        sol["estado"] = nuevo
        self.guardar()
        print("Estado actualizado a " + self.nombre_estado(nuevo))

    def asignar(self):
        print("--- Asignar responsable ---")
        id = self.pedir_numero("ID de la solicitud: ")
        if id == None:
            print("Error: el ID debe ser un numero")
            return
        sol = None
        for x in self.d["solicitudes"]:
            if x["id"] == id:
                sol = x
        if sol == None:
            print("Error: no existe la solicitud " + str(id))
            return
        if sol["estado"] == "R" or sol["estado"] == "X":
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
        if sol["estado"] == "P":
            sol["estado"] = "E"
        self.guardar()
        print("Solicitud " + str(id) + " asignada a " + RESPONSABLES[n - 1])

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
            # mostrar
            tn = ""
            if x["tipo"] == "1":
                tn = "Certificado de alumno regular"
            elif x["tipo"] == "2":
                tn = "Reclamo de nota"
            elif x["tipo"] == "3":
                tn = "Equivalencia de materias"
            elif x["tipo"] == "4":
                tn = "Excepcion de correlatividad"
            elif x["tipo"] == "5":
                tn = "Baja de materia"
            pn = ""
            if x["prioridad"] == 1:
                pn = "BAJA"
            elif x["prioridad"] == 2:
                pn = "MEDIA"
            else:
                pn = "ALTA"
            r = x["responsable"]
            if r == None:
                r = "Sin asignar"
            print("#" + str(x["id"]) + " | " + x["legajo"] + " | " + tn + " | " + pn + " | " + self.nombre_estado(x["estado"]) + " | " + r)

    def listar(self):
        print("--- Todas las solicitudes ---")
        if len(self.d["solicitudes"]) == 0:
            print("No hay solicitudes cargadas")
            return
        for x in self.d["solicitudes"]:
            tn = ""
            if x["tipo"] == "1":
                tn = "Certificado de alumno regular"
            elif x["tipo"] == "2":
                tn = "Reclamo de nota"
            elif x["tipo"] == "3":
                tn = "Equivalencia de materias"
            elif x["tipo"] == "4":
                tn = "Excepcion de correlatividad"
            elif x["tipo"] == "5":
                tn = "Baja de materia"
            pn = ""
            if x["prioridad"] == 1:
                pn = "BAJA"
            elif x["prioridad"] == 2:
                pn = "MEDIA"
            else:
                pn = "ALTA"
            r = x["responsable"]
            if r == None:
                r = "Sin asignar"
            print("#" + str(x["id"]) + " | " + x["legajo"] + " | " + tn + " | " + pn + " | " + self.nombre_estado(x["estado"]) + " | " + r)

    def reporte(self):
        print("--- Reporte ---")
        total = len(self.d["solicitudes"])
        print("Total de solicitudes: " + str(total))
        p = 0
        e = 0
        r = 0
        x = 0
        for s in self.d["solicitudes"]:
            if s["estado"] == "P":
                p = p + 1
            if s["estado"] == "E":
                e = e + 1
            if s["estado"] == "R":
                r = r + 1
            if s["estado"] == "X":
                x = x + 1
        print("Pendientes: " + str(p))
        print("En proceso: " + str(e))
        print("Resueltas: " + str(r))
        print("Rechazadas: " + str(x))
        alta = 0
        for s in self.d["solicitudes"]:
            if s["prioridad"] == 3 and s["estado"] != "R" and s["estado"] != "X":
                alta = alta + 1
        print("Abiertas con prioridad ALTA: " + str(alta))
        sin = 0
        for s in self.d["solicitudes"]:
            if s["responsable"] == None and s["estado"] != "R" and s["estado"] != "X":
                sin = sin + 1
        print("Abiertas sin responsable: " + str(sin))
        # porcentaje resueltas
        if total > 0:
            print("Porcentaje resueltas: " + str(round(r * 100 / total, 1)) + "%")
        else:
            print("Porcentaje resueltas: 0%")

    def pedir_numero(self, mensaje):
        try:
            return int(input(mensaje))
        except ValueError:
            return None

    def nombre_estado(self, e):
        if e == "P":
            return "Pendiente"
        if e == "E":
            return "En proceso"
        if e == "R":
            return "Resuelta"
        if e == "X":
            return "Rechazada"
        return "?"

    # def exportar_csv(self):
    #     f = open("export.csv", "w")
    #     for s in self.d["solicitudes"]:
    #         f.write(str(s["id"]) + "," + s["legajo"] + "\n")
    #     f.close()


if __name__ == "__main__":
    s = Sistema()
    s.menu()
