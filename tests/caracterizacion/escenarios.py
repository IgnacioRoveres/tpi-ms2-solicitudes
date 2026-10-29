"""Escenarios de caracterizacion (golden master).

Cada escenario es una secuencia de lineas que se envian por teclado al
programa (`python sistema.py`). Se ejecutan como "caja negra": solo se mira
lo que ve el usuario (la salida por pantalla) y el archivo de datos que queda
guardado. Si el refactoring no cambia el comportamiento externo, la salida
debe ser identica a la grabada sobre la version inicial (tag estado-inicial).

Todos los datos son sinteticos.
"""

# Datos de arranque reutilizados por varios escenarios
ALTA_ANA = ["1", "10001", "Ana Gomez", "ana.gomez@example.com", "2", "Reclamo por la nota del segundo parcial", "s"]
ALTA_BRUNO = ["1", "10002", "Bruno Diaz", "bruno.diaz@example.com", "1", "Necesito certificado para el trabajo", "n"]
ALTA_ANA_2 = ["1", "10001", "3", "Pedido de equivalencia de Algebra", "s"]
ALTA_CARLA = ["1", "10003", "Carla Ruiz", "carla.ruiz@example.com", "5", "Baja de Programacion II por superposicion", "n"]
CARGA_BASE = ALTA_ANA + ALTA_BRUNO + ALTA_ANA_2 + ALTA_CARLA

ESCENARIOS = {
    # --- Registro ---
    "registro_estudiante_nuevo": ALTA_ANA + ["0"],
    "registro_estudiante_existente": ALTA_ANA + ALTA_ANA_2 + ["0"],
    "registro_prioridades": [
        "1", "20001", "Dario Sosa", "dario@example.com", "1", "Certificado para la obra social", "s",
        "1", "20001", "4", "Excepcion de correlatividad Fisica", "n",
        "1", "20001", "2", "Reclamo de nota final de Quimica", "n",
        "0",
    ],
    "registro_legajo_invalido": ["1", "12ab", "1", "123", "1", "1234567", "0"],
    "registro_nombre_vacio": ["1", "30001", "", "0"],
    "registro_email_invalido": ["1", "30001", "Eva Luna", "evaexample.com", "1", "30001", "Eva Luna", "eva@examplecom", "0"],
    "registro_tipo_invalido": ["1", "30001", "Eva Luna", "eva@example.com", "9", "0"],
    "registro_descripcion_corta": ["1", "30001", "Eva Luna", "eva@example.com", "3", "corta", "0"],
    # --- Cambio de estado ---
    "estado_flujo_completo": ALTA_ANA + ["2", "1", "E", "2", "1", "R", "0"],
    "estado_rechazo_desde_pendiente": ALTA_ANA + ["2", "1", "x", "0"],
    "estado_transicion_invalida": ALTA_ANA + ["2", "1", "R", "2", "1", "P", "0"],
    "estado_cerrada_no_cambia": ALTA_ANA + ["2", "1", "X", "2", "1", "E", "0"],
    "estado_valor_invalido": ALTA_ANA + ["2", "1", "Z", "0"],
    "estado_solicitud_inexistente": ALTA_ANA + ["2", "99", "0"],
    # --- Asignacion ---
    "asignar_pendiente_pasa_a_en_proceso": ALTA_ANA + ["3", "1", "2", "0"],
    "asignar_reasignar_en_proceso": ALTA_ANA + ["3", "1", "2", "3", "1", "4", "0"],
    "asignar_responsable_invalido": ALTA_ANA + ["3", "1", "7", "3", "1", "0", "0"],
    "asignar_solicitud_cerrada": ALTA_ANA + ["2", "1", "X", "3", "1", "0"],
    "asignar_solicitud_inexistente": ["3", "5", "0"],
    # --- Busqueda ---
    "buscar_por_legajo": CARGA_BASE + ["4", "1", "10001", "0"],
    "buscar_por_estado": CARGA_BASE + ["3", "2", "1", "4", "2", "e", "4", "2", "P", "0"],
    "buscar_por_tipo": CARGA_BASE + ["4", "3", "1", "0"],
    "buscar_por_prioridad": CARGA_BASE + ["4", "4", "3", "4", "4", "1", "0"],
    "buscar_sin_resultados": CARGA_BASE + ["4", "1", "99999", "0"],
    "buscar_criterio_invalido": CARGA_BASE + ["4", "8", "x", "0"],
    # --- Listado y reporte ---
    "listar_vacio": ["5", "0"],
    "listar_con_datos": CARGA_BASE + ["3", "1", "1", "2", "1", "R", "5", "0"],
    "reporte_vacio": ["6", "0"],
    "reporte_con_datos": CARGA_BASE + ["3", "1", "2", "2", "1", "R", "2", "4", "X", "3", "2", "1", "6", "0"],
    # --- Menu ---
    "menu_opcion_invalida": ["9", "abc", "", "0"],
}
