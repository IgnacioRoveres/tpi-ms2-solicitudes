"""Criterios de busqueda (abierto a extension, cerrado a modificacion).

Agregar un criterio nuevo = agregar un miembro al enum. Ni el servicio ni
la consola cambian.
"""
from enum import Enum


class CriterioBusqueda(Enum):
    LEGAJO = ("1", "legajo", lambda solicitud, valor: solicitud.legajo == valor)
    ESTADO = ("2", "estado", lambda solicitud, valor: solicitud.estado.codigo == valor.upper())
    TIPO = ("3", "tipo", lambda solicitud, valor: solicitud.tipo.codigo == valor)
    PRIORIDAD = ("4", "prioridad", lambda solicitud, valor: str(int(solicitud.prioridad)) == valor)

    def __init__(self, codigo, etiqueta, coincide):
        self.codigo = codigo
        self.etiqueta = etiqueta
        self.coincide = coincide

    @classmethod
    def desde_codigo(cls, codigo):
        return next((c for c in cls if c.codigo == codigo), None)
