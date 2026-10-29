# Declaración de uso de inteligencia artificial

| Herramienta | Finalidad | Grado de intervención |
| --- | --- | --- |
| Claude (Anthropic), vía claude.ai | Generar el prototipo base con problemas de diseño, proponer el diagnóstico, los refactorings, las pruebas, el checklist de code review y un borrador del informe. | Alto en la producción del código y de los borradores. El equipo revisó, ejecutó y validó cada etapa y debe poder explicar y defender cada decisión. |

## Registro de prompts

| # | Fecha | Prompt (resumen fiel) | Resultado usado |
| --- | --- | --- | --- |
| 1 | 29/10/2026 | «Ayudame con esto» + la consigna del TPI (PDF), la página de la materia y el ZIP con el modelo de presentación. | El asistente preguntó cómo encarar el trabajo. |
| 2 | 29/10/2026 | Respuestas: crear un sistema nuevo (caso sugerido), en Python; pedimos código antes/después e informe completo; equipo de 2 integrantes. | Repositorio completo con tags, documentación de `docs/` e informe. |
| 3 | [completar] | [Agregar aquí cada consulta posterior: dudas, pedidos de explicación, correcciones.] | |

Evidencia: exportar la conversación completa a PDF e incluirla en el anexo ZIP (`anexo/conversacion_ia.pdf`).

## Qué verificó el equipo

- [ ] Ejecutamos `python sistema.py` y probamos las 6 opciones.
- [ ] Ejecutamos `python -m pytest` (99 pruebas en verde).
- [ ] Recorrimos `git log` y entendimos qué hace cada commit de refactoring.
- [ ] Cada integrante puede explicar al menos: un smell, un principio SOLID aplicado, un refactoring y cómo se verificó.
