# Sistema de Gestión de Solicitudes Académicas (SGSA)

Trabajo Práctico Integrador — **Metodología de Sistemas II**
Tecnicatura Universitaria en Programación a Distancia.

Sistema de consola que registra las solicitudes de los estudiantes (certificados, reclamos de nota, equivalencias, excepciones de correlatividad y bajas de materia), las clasifica por tipo y prioridad, sigue su estado y las asigna a un área responsable.

El objetivo del trabajo no es la funcionalidad sino la **evolución de la calidad interna**: se parte de una versión inicial que funciona pero está mal diseñada, se la diagnostica y se la refactoriza sin alterar el comportamiento externo.

## Integrantes

| Integrante | GitHub | Aporte principal |
| --- | --- | --- |
| Ignacio Roveres | [@IgnacioRoveres](https://github.com/IgnacioRoveres) | Estructura inicial, golden master, enums (R1), Move Method (R3), Extract Class/DIP (R5) |
| Nidia Samaniego | [@usuario] | Versión inicial, diagnóstico, fix S7/S8, Extract Method (R2), Parameter Object (R4), pruebas unitarias, correcciones del code review |

## Funcionalidades

1. Registrar solicitud (con validación de legajo, nombre, email, tipo y descripción; reutiliza los datos de estudiantes ya cargados).
2. Cambiar estado: Pendiente → En proceso → Resuelta o Rechazada.
3. Asignar responsable (Bedelía, Secretaría Académica, Tesorería, Coordinación de Carrera).
4. Buscar por legajo, estado, tipo o prioridad.
5. Listar todas.
6. Reporte: totales por estado, abiertas con prioridad ALTA, abiertas sin responsable y % de resueltas.

Prioridad automática: reclamo de nota = ALTA, certificado = BAJA, resto = MEDIA; si es urgente, sube un nivel.

## Tecnologías

Python 3.10 o superior (solo biblioteca estándar) · JSON para persistencia · pytest y pytest-cov · pyflakes y radon para análisis estático · Git y GitHub.

## Instalación y uso

```bash
git clone https://github.com/IgnacioRoveres/tpi-ms2-solicitudes.git
cd tpi-ms2-solicitudes
python sistema.py            # los datos se guardan en ./solicitudes.json
```

Para correr las pruebas:

```bash
pip install -r requirements-dev.txt
python -m pytest                              # 99 pruebas
python -m pytest --cov=sgsa                   # con cobertura
bash docs/evidencias/verificar_commits.sh     # golden master contra cada commit
```

## Estructura

```
sistema.py                  punto de entrada (raíz de composición)
sgsa/
  dominio.py                Estado, Prioridad, TipoSolicitud (enums + reglas)
  modelos.py                Solicitud, Estudiante
  dto.py                    NuevaSolicitud (parameter object)
  validaciones.py           ValidadorSolicitud
  errores.py                excepciones de negocio
  busqueda.py               CriterioBusqueda
  reporte.py                cálculo del resumen
  repositorio.py            RepositorioSolicitudes, RepositorioJSON, RepositorioEnMemoria
  servicio.py               ServicioSolicitudes (casos de uso)
  consola.py                interfaz de usuario
  formato.py                presentación en texto
tests/
  caracterizacion/          golden master (30 escenarios, caja negra)
  unitarias/                pruebas por capa
  test_mejoras_comportamiento.py
docs/
  diagnostico.md            calidad externa/interna y 14 code smells
  decisiones.md             arquitectura, decisiones y métricas
  code_review.md            checklist, observaciones y criterios de aceptación
  uso_ia.md                 declaración de uso de IA
  evidencias/               salidas de pruebas, radon y golden por commit
```

## Versiones y etapas (tags)

| Tag | Contenido |
| --- | --- |
| `estado-inicial` | Versión base, un solo archivo con los problemas de diseño |
| `etapa-diagnostico` | Diagnóstico y golden master |
| `etapa-refactoring` | Refactorings R1 a R5 aplicados |
| `etapa-pruebas` | Pruebas unitarias y evidencias |
| `etapa-docs` | Code review y documentación |
| `estado-refactorizado` | Versión final |

Para ver la versión inicial: `git checkout estado-inicial`. Para comparar: `git diff estado-inicial estado-refactorizado -- sistema.py`.

## Uso de IA

Se usó un asistente de IA como apoyo. Ver `docs/uso_ia.md`.
