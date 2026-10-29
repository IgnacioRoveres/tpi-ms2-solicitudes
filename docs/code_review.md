# Code review — versión refactorizada

- **Alcance revisado:** todos los commits entre los tags `etapa-diagnostico` y `etapa-pruebas` (de `fix: manejo de entrada…` a `test: pruebas unitarias…`).
- **Autores del código:** Integrante 1 e Integrante 2. Revisión cruzada: cada integrante revisó los commits del otro.
- **Herramientas de apoyo:** `pytest` + `pytest-cov`, `pyflakes` (análisis estático) y `radon` (complejidad ciclomática e índice de mantenibilidad).
- **Resultado:** aprobado con 5 correcciones aplicadas (commit `fix(review): correcciones del code review CR-01 a CR-05`), 1 corrección de lint y 3 observaciones aceptadas con justificación.

## 1. Checklist técnico

| # | Área | Criterio | Resultado | Evidencia |
| --- | --- | --- | --- | --- |
| 1 | Comportamiento | El golden master pasa 30/30 en cada commit del refactoring | Cumple | `docs/evidencias/golden_por_commit.md` |
| 2 | Comportamiento | Cada cambio de comportamiento es intencional, está documentado y tiene prueba | Cumple | `tests/test_mejoras_comportamiento.py` |
| 3 | SRP | Cada módulo tiene un único motivo de cambio | Cumple | dominio, servicio, repositorio, consola, formato |
| 4 | OCP | Agregar estado, tipo, criterio u opción de menú no exige modificar condicionales | Cumple | Enums + tabla de transiciones + tabla de opciones |
| 5 | LSP | Las implementaciones del repositorio son intercambiables | Cumple | `test_repositorio.py` corre el mismo contrato sobre las dos |
| 6 | ISP | Ningún cliente depende de métodos que no usa | Cumple | `resumir()` recibe un iterable, no el repositorio |
| 7 | DIP | La lógica depende de abstracciones, no de E/S concreta | Cumple | `ServicioSolicitudes(repositorio)`, `ConsolaSolicitudes(entrada, salida)` |
| 8 | Nombres | Nombres expresivos, sin abreviaturas de una letra, sin ocultar funciones nativas | Cumple | — |
| 9 | Funciones | Ningún método supera complejidad ciclomática 10 | Cumple | `radon`: máximo 10 (`resumir`), antes 23 |
| 10 | Errores | No hay `except` genérico; los errores de negocio son excepciones con nombre | Cumple | `sgsa/errores.py` |
| 11 | Persistencia | Un corte durante el guardado no deja el archivo inconsistente | **No cumplía** → CR-01 | — |
| 12 | Valores mágicos | No quedan literales con significado de negocio en el código | **Parcial** → CR-02 | `"s"` en la consola |
| 13 | Cohesión | El formato de pantalla está en `formato.py` | **Parcial** → CR-03 | criterios formateados en la consola |
| 14 | Inmutabilidad | Las reglas de negocio no se pueden alterar en ejecución | **No cumplía** → CR-04 | `dict` y `set` mutables |
| 15 | Legibilidad de la API | Los métodos públicos del servicio declaran tipos | **No cumplía** → CR-05 | — |
| 16 | Pruebas | Cobertura ≥ 85 % del paquete `sgsa` | Cumple | 92 % (`docs/evidencias/pytest_final.txt`) |
| 17 | Análisis estático | `pyflakes` sin advertencias | **No cumplía** → corregido | import sin uso en una prueba |
| 18 | Repositorio | Commits atómicos, mensajes descriptivos y tags de etapa | Cumple | `git log --oneline --decorate` |
| 19 | Datos | Solo datos sintéticos | Cumple | `tests/caracterizacion/escenarios.py` |

## 2. Observaciones y acciones

| ID | Archivo | Observación (feedback) | Severidad | Acción | Estado |
| --- | --- | --- | --- | --- | --- |
| CR-01 | `sgsa/repositorio.py` | `write_text` escribe directo sobre el archivo. Si el programa se corta a la mitad, el JSON queda truncado y la próxima ejecución lo rechaza como dañado. | Alta | Escribir en `solicitudes.json.tmp` y reemplazar con `os.replace` (atómico). Prueba `test_json_no_deja_archivos_temporales`. | Corregido en `fix(review)` |
| CR-02 | `sgsa/consola.py` | `== "s"` es un literal con significado. Si se cambia la pregunta a «S/N» hay que buscarlo. | Baja | Constante `RESPUESTA_SI`. | Corregido en `fix(review)` |
| CR-03 | `sgsa/consola.py` | El texto «1. Por legajo 2. Por estado…» se arma en la consola, mientras que los otros formatos están en `formato.py`. | Baja | Nueva función `formatear_criterios()`. | Corregido en `fix(review)` |
| CR-04 | `sgsa/dominio.py` | `_TRANSICIONES_PERMITIDAS` es un `dict` de `set` mutables: cualquier módulo podría alterar el ciclo de vida. | Media | `MappingProxyType` + `frozenset`. Prueba `test_reglas_de_transicion_son_de_solo_lectura`. | Corregido en `fix(review)` |
| CR-05 | `sgsa/servicio.py` | La API pública no declara tipos; quien la use desde otra interfaz tiene que leer el código. | Baja | Anotaciones de tipo en todos los métodos públicos. | Corregido en `fix(review)` |
| CR-06 | `tests/test_mejoras_comportamiento.py` | `pyflakes`: `Path` importado y sin uso. | Baja | Se elimina el import. | Corregido en `docs: code review…` |
| CR-07 | `sgsa/repositorio.py` | `RepositorioJSON` hereda de `RepositorioEnMemoria`. ¿No sería mejor composición? | Media | **Aceptado como está.** La herencia es por especialización real (memoria + volcado a disco, gancho `_al_modificar`) y la prueba de contrato confirma la sustitución (LSP). Se revisará si aparece otro tipo de almacenamiento. | Aceptado |
| CR-08 | `sgsa/repositorio.py` | `obtener()` devuelve el objeto interno; un cliente podría modificarlo sin llamar a `actualizar()`. | Media | **Aceptado.** Solo el servicio usa el repositorio y siempre llama a `actualizar()`. Queda como mejora futura (copias o unidad de trabajo). | Aceptado |
| CR-09 | Todo el proyecto | Los mensajes no llevan tildes («Opcion», «danado»). | Baja | **Aceptado.** Cambiarlos modificaría la salida que ve el usuario y rompería el golden master. Es un cambio funcional y debe pedirlo el usuario; queda como mejora futura con su propio commit. | Aceptado |

## 3. Criterios de aceptación técnica

Un cambio se acepta en `main` solo si cumple todo lo siguiente:

1. `python -m pytest` pasa completo (golden master + unitarias + mejoras).
2. El golden master no se regraba: si cambia la salida, el cambio debe ser intencional y tener su propia prueba en `test_mejoras_comportamiento.py`.
3. `python -m pyflakes sgsa sistema.py tests` no informa advertencias.
4. Ningún método nuevo supera complejidad ciclomática 10 (`radon cc -n C sgsa` no lista nada).
5. Cobertura de `sgsa` ≥ 85 %.
6. No se agregan `print`/`input` fuera de `consola.py` ni `open`/`json` fuera de `repositorio.py`.
7. Mensaje de commit con prefijo (`feat`, `fix`, `refactor`, `test`, `docs`) y referencia al smell u observación (`S4`, `CR-01`).
8. Revisión aprobada por el otro integrante.
