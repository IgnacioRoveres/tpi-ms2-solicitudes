"""Calculo del reporte, separado de su presentacion por pantalla."""
from dataclasses import dataclass

from sgsa.dominio import Estado, Prioridad


@dataclass(frozen=True)
class ResumenSolicitudes:
    total: int
    por_estado: dict
    abiertas_prioridad_alta: int
    abiertas_sin_responsable: int

    @property
    def porcentaje_resueltas(self):
        """Porcentaje con un decimal, o None si no hay solicitudes."""
        if self.total == 0:
            return None
        return round(self.por_estado[Estado.RESUELTA] * 100 / self.total, 1)


def resumir(solicitudes):
    """Recibe solo un iterable de solicitudes: no depende del repositorio (ISP)."""
    solicitudes = list(solicitudes)
    abiertas = [s for s in solicitudes if s.esta_abierta]
    return ResumenSolicitudes(
        total=len(solicitudes),
        por_estado={estado: sum(1 for s in solicitudes if s.estado is estado) for estado in Estado},
        abiertas_prioridad_alta=sum(1 for s in abiertas if s.prioridad is Prioridad.ALTA),
        abiertas_sin_responsable=sum(1 for s in abiertas if s.responsable is None),
    )
