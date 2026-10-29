"""La consola se prueba sin teclado gracias a entrada/salida inyectadas."""
from datetime import date

from sgsa.consola import ConsolaSolicitudes
from sgsa.repositorio import RepositorioEnMemoria
from sgsa.servicio import ServicioSolicitudes


def correr(entradas):
    pendientes = iter(entradas)
    salida = []
    servicio = ServicioSolicitudes(RepositorioEnMemoria(), hoy=lambda: date(2026, 10, 29))
    consola = ConsolaSolicitudes(servicio, entrada=lambda _mensaje: next(pendientes), salida=salida.append)
    consola.ejecutar()
    return salida, servicio


def test_registro_y_listado():
    salida, servicio = correr(["1", "10001", "Ana Gomez", "ana@example.com", "2", "Reclamo por la nota final", "n", "5", "0"])
    assert "Solicitud registrada con ID 1" in salida
    assert "#1 | 10001 | Reclamo de nota | ALTA | Pendiente | Sin asignar" in salida
    assert len(servicio.listar()) == 1


def test_errores_de_negocio_se_muestran_y_el_menu_sigue():
    salida, _ = correr(["2", "x", "3", "8", "4", "9", "", "0"])
    assert "Error: el ID debe ser un numero" in salida
    assert "Error: no existe la solicitud 8" in salida
    assert "Error: criterio invalido" in salida
    assert salida[-1] == "Hasta luego"


def test_menu_se_arma_desde_la_tabla_de_opciones():
    salida, _ = correr(["0"])
    assert salida[2:9] == ["1. Registrar solicitud", "2. Cambiar estado", "3. Asignar responsable",
                           "4. Buscar solicitudes", "5. Listar todas", "6. Reporte", "0. Salir"]
