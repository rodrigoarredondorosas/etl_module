RELATION = [
    # Pabellón [Citas, Registro Clínico, Órden QX, Tabla QX, Presupuesto QX]
    {"r_id": 1, "use_case": 2, "steps": [1, 3, 7, 8, 9]},
]

RELATION_FIELDS = [
    # Pabellón
    {
        # Citas
        "rf_id": 1,
        "r_id": 1,
        "step_id": 1,
        "fields": [1, 2, 38, 40, 5, 6, 7, 8, 9, 39, 10, 11, 12],
        "required_fields": [1, 2, 38, 40, 5, 6, 7, 8, 9, 10],
        "required_relation_fields": None,
        "foreign_keys": [],
    },
    {
        # Registro Clínico
        "rf_id": 2,
        "r_id": 1,
        "step_id": 3,
        "fields": [15, 16, 904, 903, 11, 9,68,69],
        "required_fields": [15, 16],
        "required_relation_fields": None,
        "foreign_keys": [],
    },
    {
        # Órden QX
        "rf_id": 3,
        "r_id": 1,
        "step_id": 7,
        "fields": [45, 900, 4, 9, 46, 23, 47, 48, 44, 49],
        "required_fields": [4, 9, 23, 45, 46, 47, 48],
        "required_relation_fields": None,
        "foreign_keys": [],
    },
    {
        # Tabla QX
        "rf_id": 4,
        "r_id": 1,
        "step_id": 8,
        # 50 - ID Tabla QX
        # 900 - ID Cita
        # 11 - Usuario Creación
        # 16 - Fecha y Hora Creación
        # 9 - Paciente
        # 51 - Observación Interna
        # 903 - Orden QX
        # 52 - Folio
        # 53 - Cirujano Principal
        # 54 - Anestesista
        # 55 - Ayudante
        # 56 - Estado QX
        # 57 - Estado Cuenta Médica
        # 58 - RUT Prestador
        # 59 - Unidad
        # 60 - Recurso Pabellón
        "fields": [50, 900, 11, 16, 9, 51, 903, 52, 53, 54, 55, 56, 57, 58, 59, 60],
        "required_fields": [50, 900, 9, 53, 903, 16],
        "required_relation_fields": None,
        "foreign_keys": [],
    },
    {
        # Presupuesto QX
        "rf_id": 5,
        "r_id": 1,
        "step_id": 9,
        # 61 - ID Presupuesto QX
        # 903 - ID Órden QX
        # 11 - Usuario Creación
        # 16 - Fecha y Hora Creación
        # 9 - Paciente
        # 62 - Nombre de Presupuesto
        # 2 - Sucursal
        # 63 - Estado Presupuesto
        # 64 - Modalidad Presupuesto
        # 58 - RUT Prestador
        # 48 - Lateralidad
        # 65 - Código Prestación
        # 66 - Cantidad
        # 67 - Precio
        "fields": [61, 903, 11, 16, 9, 62, 2, 63, 64, 58, 48, 65, 66, 67],
        "required_fields": [61,16, 903, 62,2, 63, 64, 58, 65, 66, 67],
        "required_relation_fields": None,
        "foreign_keys": [],
    },
]

RELATION_FIELDS_FORMATS = [
    {
        "rf_id": [1, 2, 4, 5],
        "field": 9,
        "formats": [1],
    },
    {
        "rf_id": [2],
        "field": 4,
        "formats": [1],
    },
]


RELATION_FIELDS_RESTRICTIONS = []
