RELATION = [
    # Exámen [Citas, Órden de Exámen]
    {"r_id": 1, "use_case": 6, "steps": [1, 5]},
]

RELATION_FIELDS = [
    # Exámen
    {
        # Citas
        "rf_id": 1,
        "r_id": 1,
        "step_id": 1,
        "fields": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 36, 11, 37],
        "required_fields": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 36],
        "required_relation_fields": None,
        "foreign_keys": [],
    },
    {
        # Órden de Exámen
        "rf_id": 1,
        "r_id": 1,
        "step_id": 5,
        "fields": [33, 901, 900, 4, 9, 23, 34, 35, 36],
        "required_fields": [33, 901, 34, 35, 36],
        "required_relation_fields": None,
        "foreign_keys": [901, 900],
    },
]

RELATION_FIELDS_FORMATS = [
    {
        "rf_id": [1],
        "field": 4,
        "formats": [1],
    },
    {
        "rf_id": [1],
        "field": 9,
        "formats": [1],
    },
]


RELATION_FIELDS_RESTRICTIONS = []
