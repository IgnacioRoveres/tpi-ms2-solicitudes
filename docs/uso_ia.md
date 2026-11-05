# Declaración de uso de inteligencia artificial

| Herramienta | Finalidad | Grado de intervención |
| --- | --- | --- |
| Claude (Anthropic), vía claude.ai | Generar el prototipo base con problemas de diseño, el diagnóstico, los refactorings, las pruebas, el checklist de code review, los borradores del informe y materiales de estudio (guía y guion del video). | Alto en la producción del código y de los borradores. El equipo revisó, ejecutó y validó cada etapa, y debe poder explicar y defender cada decisión. |

## Registro de prompts

| # | Fecha | Prompt (resumen fiel) | Resultado usado |
| --- | --- | --- | --- |
| 1 | 29/10/2026 | «Ayudame con esto» + la consigna del TPI (PDF), la página de la materia y el ZIP con el modelo de presentación. | El asistente preguntó cómo encarar el trabajo (sistema, lenguaje, alcance, equipo). |
| 2 | 29/10/2026 | Respuestas: crear un sistema nuevo (caso sugerido), en Python; pedimos código antes/después e informe completo; equipo de 2 integrantes. | Repositorio completo con tags, documentación de `docs/` e informe. |
| 3 | 29/10/2026 | Pedido de una guía con contexto para explicarle el trabajo. | Guía de estudio con explicaciones, reparto y preguntas probables. |
| 4 | 30/10/2026 | Pedido de los archivos para compartir entre los integrantes. | Exportación de la guía (PDF) y del informe (Word). |
| 5 | 04/11/2026 | Datos de los integrantes para asignar la autoría de los commits. | Commits y tags a nombre de cada integrante. |
| 6 | 04/11/2026 | Pedido de un guion del video por cada cambio. | Guion con un bloque por commit. |

Evidencia: conversación completa exportada a PDF en el anexo (`anexo/conversacion_ia.pdf`).

## Qué verificó el equipo

- [ ] Ejecutamos `python sistema.py` y probamos las 6 opciones.
- [ ] Ejecutamos `python -m pytest` (99 pruebas en verde).
- [ ] Recorrimos `git log` y entendimos qué hace cada commit de refactoring.
- [ ] Cada integrante puede explicar al menos: un smell, un principio SOLID aplicado, un refactoring y cómo se verificó.