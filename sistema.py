"""Sistema de Gestion de Solicitudes Academicas - punto de entrada.

Arma las dependencias (raiz de composicion) y arranca la consola.
Uso: python sistema.py
"""
import sys
from pathlib import Path

from sgsa.consola import ConsolaSolicitudes
from sgsa.errores import DatosCorruptos
from sgsa.repositorio import RepositorioJSON
from sgsa.servicio import ServicioSolicitudes

ARCHIVO_DATOS = Path("solicitudes.json")


def main():
    try:
        repositorio = RepositorioJSON(ARCHIVO_DATOS)
    except DatosCorruptos as error:
        print(f"Error: {error}")
        return 1
    ConsolaSolicitudes(ServicioSolicitudes(repositorio)).ejecutar()
    return 0


if __name__ == "__main__":
    sys.exit(main())
