"""Como se muestran las solicitudes y el reporte (solo texto, sin logica)."""
from sgsa.dominio import Estado

SIN_RESPONSABLE = "Sin asignar"


def formatear_solicitud(solicitud):
    return " | ".join([
        f"#{solicitud.id}",
        solicitud.legajo,
        solicitud.tipo.etiqueta,
        solicitud.prioridad.etiqueta,
        solicitud.estado.etiqueta,
        solicitud.responsable or SIN_RESPONSABLE,
    ])


def formatear_resumen(resumen):
    porcentaje = resumen.porcentaje_resueltas
    return [
        f"Total de solicitudes: {resumen.total}",
        f"Pendientes: {resumen.por_estado[Estado.PENDIENTE]}",
        f"En proceso: {resumen.por_estado[Estado.EN_PROCESO]}",
        f"Resueltas: {resumen.por_estado[Estado.RESUELTA]}",
        f"Rechazadas: {resumen.por_estado[Estado.RECHAZADA]}",
        f"Abiertas con prioridad ALTA: {resumen.abiertas_prioridad_alta}",
        f"Abiertas sin responsable: {resumen.abiertas_sin_responsable}",
        f"Porcentaje resueltas: {0 if porcentaje is None else porcentaje}%",
    ]


def formatear_opciones(opciones):
    """Une pares (codigo, etiqueta) como 'P-Pendiente E-En proceso'."""
    return " ".join(f"{codigo}-{etiqueta}" for codigo, etiqueta in opciones)


def formatear_criterios(criterios):
    """Une criterios como '1. Por legajo 2. Por estado'."""
    return " ".join(f"{c.codigo}. Por {c.etiqueta}" for c in criterios)
