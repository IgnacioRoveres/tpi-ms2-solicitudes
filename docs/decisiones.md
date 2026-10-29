# Decisiones técnicas

## Arquitectura resultante

```
sistema.py  (raíz de composición: arma las dependencias)
   │
   ▼
consola.py ──► servicio.py ──► RepositorioSolicitudes (abstracción)
   │              │                 ├── RepositorioJSON      (programa)
   │              │                 └── RepositorioEnMemoria (pruebas)
   ▼              ▼
formato.py     modelos.py / dominio.py / busqueda.py / reporte.py
               validaciones.py / dto.py / errores.py
```

Las dependencias van hacia adentro: el dominio no conoce a nadie; el servicio conoce el dominio y la abstracción del repositorio; solo la consola hace E/S de pantalla y solo el repositorio toca archivos.

## Decisiones

| # | Decisión | Alternativa descartada | Motivo |
| --- | --- | --- | --- |
| D1 | Golden master (caja negra por subprocess) como red de seguridad **antes** de refactorizar | Escribir pruebas unitarias primero | La versión inicial no tenía unidades probables: todo dependía de `input`/`print`. La caja negra no depende de la estructura interna, así que sirve sin cambios antes y después. |
| D2 | Corregir S7/S8 en un commit propio, antes del refactoring | Corregirlos durante el refactoring | Un refactoring no debe cambiar comportamiento. Separarlos deja claro qué commit cambia la conducta (fix) y cuáles no (refactor). |
| D3 | Enums con `codigo` que se guarda en el JSON | Guardar el nombre del enum (`"PENDIENTE"`) | Mantener el formato del archivo: los datos existentes siguen funcionando (prueba `test_json_lee_archivos_de_la_version_inicial`). |
| D4 | Mantener los textos de pantalla sin tildes | Corregir la ortografía | Es comportamiento externo. Ver CR-09. |
| D5 | Validación por campo en la consola y validación completa en el servicio | Validar solo en el servicio | La consola original corta en el primer dato inválido sin pedir los siguientes; hay que conservarlo. El servicio valida igual para no depender de la interfaz. |
| D6 | `hoy` y `responsables` inyectables en el servicio | `date.today()` y lista global | Pruebas deterministas y catálogo extensible (resuelve S10). |
| D7 | Persistencia: volcado completo con escritura atómica | Base de datos SQLite | El volumen es chico y el alcance del TP es la calidad interna; la abstracción permite cambiarlo después sin tocar el servicio. |

## Métricas antes / después (radon)

| Métrica | Inicial | Refactorizada |
| --- | --- | --- |
| Archivos de código | 1 | 13 |
| Líneas de código (LOC) | 320 | 745 (incluye docstrings) |
| Complejidad ciclomática máxima | 23 (`buscar`) | 10 (`resumir`) |
| Complejidad ciclomática promedio | 8,7 (B) | 1,9 (A) |
| Índice de mantenibilidad (peor archivo) | 19,7 | 47,8 (`consola.py`) |
| Pruebas automatizadas | 0 | 99 |

El código creció en líneas, y es esperable: se separaron responsabilidades y se agregaron docstrings. Lo que importa es que bajó la complejidad por método, que es lo que determina el costo de entender y cambiar cada parte.
