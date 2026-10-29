# Diagnóstico de calidad — versión inicial (tag `estado-inicial`)

Archivo analizado: `sistema.py` (320 líneas, 1 clase, 13 métodos).
Las líneas citadas corresponden al tag `estado-inicial`.

## Calidad externa (lo que ve el usuario)

| Funcionalidad | Resultado observado |
| --- | --- |
| Registrar solicitud (con validaciones) | Funciona. Valida legajo, nombre, email, tipo y descripción. |
| Cambiar estado | Funciona y respeta el ciclo Pendiente → En proceso → Resuelta/Rechazada. |
| Asignar responsable | Funciona. Una solicitud pendiente pasa a "En proceso". |
| Buscar por legajo, estado, tipo o prioridad | Funciona. |
| Listar y reporte | Funcionan. |
| ID no numérico al cambiar estado / asignar | **Falla**: el programa termina con `ValueError` (traceback). |
| Archivo de datos dañado | **Falla silenciosa**: se ignora el error y el siguiente guardado **pisa los datos** (pérdida total). |

## Calidad interna — code smells y deuda técnica

Prioridad: **A** = alta (corregir primero), **M** = media, **B** = baja.

| # | Smell / debilidad | Ubicación | Evidencia | Impacto | Riesgo de mantenimiento | Prioridad |
| --- | --- | --- | --- | --- | --- | --- |
| S1 | God Class | `Sistema` (l. 15-309) | Una clase hace menú, entrada/salida, validación, reglas de negocio, persistencia y reportes. | Cualquier cambio toca la misma clase; imposible probar la lógica sin la consola. | Alto | A |
| S2 | Long Method | `registrar_solicitud()` (l. 65-106) | 42 líneas: pide datos, valida 5 campos, calcula prioridad y delega el alta. Comentarios `# validar legajo`, `# calcular prioridad` marcan bloques extraíbles. | Difícil de leer y de probar por partes. | Alto | A |
| S3 | Duplicated Code | Formateo de fila: `buscar()` l. 209-232 y `listar()` l. 239-261. Búsqueda por ID: l. 128-131 y l. 157-160. Filtro de "abiertas": l. 286 y l. 291. | Bloques idénticos copiados. | Un cambio de formato o de regla se debe repetir en varios lugares; alto riesgo de inconsistencias. | Alto | A |
| S4 | Primitive Obsession / valores mágicos | Estados `"P"`, `"E"`, `"R"`, `"X"` (l. 118, 138, 143-146, 272-279); prioridad `1/2/3` (l. 96-105); tipos `"1"`…`"5"` (l. 87, 211-220); solicitudes como `dict` | El significado de los códigos está repartido en el código. | Errores de tipeo no detectados; agregar un estado o tipo exige buscar todas las apariciones. | Alto | A |
| S5 | Switch Statements (violación de OCP) | Cadenas `if/elif` de tipos (l. 211-220, 240-249), prioridades (l. 222-228, 251-257), `nombre_estado()` (l. 300-309), transiciones (l. 142-146), criterios de búsqueda (l. 187-205) | Toda variación se resuelve con condicionales. | Agregar un tipo, estado o criterio obliga a modificar código existente en 3-4 lugares. | Medio | M |
| S6 | Long Parameter List | `crear_solicitud(legajo, nombre, email, t, desc, urgente, p, fecha)` (l. 108) | 8 parámetros posicionales, varios del mismo tipo. | Fácil invertir argumentos sin que falle nada. | Medio | M |
| S7 | Excepción silenciada | `cargar()` l. 27: `except: pass` | Captura todo (incluso errores de programación) y no informa nada. | **Pérdida de datos** comprobada: un JSON dañado se sobrescribe en el próximo guardado. | Crítico | A |
| S8 | Manejo de errores ausente en la entrada | `int(input(...))` en l. 127, 156, 171 | Una letra en lugar de un número corta el programa. | Mala experiencia de usuario; el error no está contemplado en el diseño. | Alto | A |
| S9 | Estado global mutable | `datos` (l. 12), `RESPONSABLES` (l. 10), `self.d = datos` (l. 18) | Todas las instancias comparten el mismo diccionario. | Efectos colaterales entre instancias; pruebas acopladas entre sí. | Medio | M |
| S10 | Número mágico acoplado | `if n < 1 or n > 4` (l. 172) | El 4 depende del largo de `RESPONSABLES`. | Agregar un responsable lo deja inaccesible sin que nada avise. | Medio | M |
| S11 | Nombres poco expresivos | `d`, `t`, `p`, `l`, `x`, `c`, `v`, `urg`, `tn`, `pn`, `sin`; `id` oculta la función nativa (l. 127) | El lector debe deducir el significado. | Mayor tiempo de comprensión y errores al modificar. | Medio | M |
| S12 | Acoplamiento a infraestructura (violación de DIP) | `open()`/`json` dentro de la clase de negocio (l. 21-33); `print`/`input` mezclados con reglas | La lógica depende de la consola y del archivo concretos. | No se puede cambiar el almacenamiento ni reutilizar la lógica (p. ej. en una web). Archivos abiertos sin `with`. | Alto | A |
| S13 | Código muerto | `exportar_csv()` comentado (l. 311-315) | Código comentado sin uso. | Ruido y confusión sobre qué está vigente. | Bajo | B |
| S14 | Comentarios que reemplazan nombres | `# validar legajo` (l. 68), `# calcular prioridad` (l. 95), `# mostrar` (l. 210), `# reglas de transicion` (l. 141) | El comentario explica lo que un método bien nombrado diría solo. | Comentarios que se desactualizan. | Bajo | B |

## Orden de corrección decidido

1. Red de seguridad: pruebas de caracterización (golden master) sobre la versión inicial.
2. S7 y S8 (riesgo para el usuario), con su propio commit y prueba, porque **cambian** el comportamiento a propósito (lo mejoran).
3. S4/S5 → enums de dominio; S3 → un único formateador y búsqueda por ID.
4. S2/S6 → Extract Method + Introduce Parameter Object.
5. S1/S12/S9 → separar capas (dominio, servicio, repositorio, consola) e inyectar dependencias.
6. S10, S11, S13, S14 → limpieza final.
