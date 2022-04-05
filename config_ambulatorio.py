RELATION = [
    # Ambulatorio [Citas, Registro Clínico, Recetas]
    {"r_id": 1, "use_case": 1, "steps": [1, 3, 4, 6]},
]

RELATION_FIELDS = [
    # Ambulatorio
    {
        # Citas
        "rf_id": 1,
        "r_id": 1,
        "step_id": 1,
        "fields": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 14, 12, 13],
        "required_fields": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
        "required_relation_fields": None,
        "foreign_keys": [],
    },
    {
        # Registro Clínico
        "rf_id": 2,
        "r_id": 1,
        "step_id": 3,
        "fields": [15, 900, 16, 17, 18, 19, 20, 21],
        "required_fields": [15, 1, 16, 17, 18, 900],
        "required_relation_fields": [{"if": 19, "then": [20]}],
        "foreign_keys": [900],
    },
    {
        # Recetas
        "rf_id": 3,
        "r_id": 1,
        "step_id": 4,
        "fields": [22, 900, 4, 9, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32],
        "required_fields": [900, 4, 9, 22, 23, 24, 25, 27, 28, 29, 31],
        "required_relation_fields": None,
        "foreign_keys": [900],
    },
    {
        # Interconsultas
        "rf_id": 4,
        "r_id": 1,
        "step_id": 6,
        "fields": [41, 901, 900, 9, 4, 23, 42, 43, 44],
        "required_fields": [901, 42],
        "required_relation_fields": None,
        "foreign_keys": [900, 9, 4],
    },
]

RELATION_FIELDS_FORMATS = [
    {
        "rf_id": [1, 3],
        "field": 4,
        "formats": [1],
    },
    {
        "rf_id": [1, 3],
        "field": 9,
        "formats": [1],
    },
]


RELATION_FIELDS_RESTRICTIONS = [
    {
        "rf_id": [1],
        "field": 8,
        "restrictions": [1],
    },
]
