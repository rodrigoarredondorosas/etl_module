# CONS

ID_MEDINET = "ID MEDINET"

VIA = (
    (1, "Oral"),
    (2, "Sublingual"),
    (3, "Bucal"),
    (4, "Tópica"),
    (5, "Transdérmica"),
    (6, "Inhalación"),
    (7, "Instilación"),
    (8, "Ocular"),
    (9, "Rectal"),
    (10, "Vaginal"),
    (11, "Parenteral Subcutánea"),
    (12, "Parenteral Intramuscular"),
    (13, "Parenteral Endovenosa"),
)

PERIODO_TIEMPO = ((1, "Minutos"), (2, "Horas"), (3, "Días"))

ESTADOS_DIAG = ((1, "Sospecha"), (2, "Vigente"), (3, "No vigente"))

TIPO_ORDEN = (("False", "Interno"), ("True", "Externo"))

TIPO_REGISTRO = (
    ("Pre-operatorio", "Pre-operatorio"),
    ("Intervención", "Intervención"),
    ("Post-operatorio", "Post-operatorio"),
)

# CONFIG VARIABLES

USE_CASES = [
    {"u_id": 1, "name": "Ambulatorio"},
    {"u_id": 2, "name": "Pabellón"},
    {"u_id": 6, "name": "Exámenes"},
]

STEPS = [
    # General
    {"step_id": 1, "name": "Citas", "excel_name": "citas"},
    {"step_id": 3, "name": "Registro Clínico", "excel_name": "registro_clinico"},
    # Ambulatorio
    {"step_id": 4, "name": "Recetas", "excel_name": "recetas"},
    {"step_id": 6, "name": "Interconsultas", "excel_name": "interconsultas"},
    # Examen
    {"step_id": 5, "name": "Órden de Exámen", "excel_name": "orden_examen"},
    # Quirúrgico
    {"step_id": 7, "name": "Órden Quirúrgica", "excel_name": "orden_quirurgica"},
    {"step_id": 8, "name": "Tabla Quirúrgica", "excel_name": "tabla_quirurgica"},
    {
        "step_id": 9,
        "name": "Presupuesto Quirúrgico",
        "excel_name": "presupuesto_quirurgico",
    },
]

# CLIENT
MOCKUP_CLIENT = {
    "use_case": 2,
    "step": 9,
    "schema": "schema156294258446voxxxm",
    "document": "excel_presupuesto_quirurgico.xlsx",
}

FIELDS = [
    # Foreign Keys
    {
        "field_id": 900,
        "name": "ID Cita",
        "type": str,
        "choices": None,
        "db": {
            "table": "agenda_cita",
            "column": "external_id",
            "return": "id",
            "condition": True,
        },
    },
    {
        "field_id": 901,
        "name": "ID Registro Clínico",
        "type": str,
        "choices": None,
        "db": {
            "table": "pacientes_registro",
            "column": "external_id",
            "return": "id",
            "condition": True,
        },
    },
    {
        "field_id": 902,
        "name": "ID Órden Examen",
        "type": str,
        "choices": None,
        "db": {
            "table": "pacientes_ordenmedica",
            "column": "external_id",
            "return": "id",
            "condition": True,
        },
    },
    {
        "field_id": 903,
        "name": "ID Órden QX",
        "type": str,
        "choices": None,
        "db": {
            "table": "hospital_ordenquirurgica",
            "column": "external_id",
            "return": "id",
            "condition": True,
        },
    },
    {
        "field_id": 904,
        "name": "ID Tabla QX",
        "type": str,
        "choices": None,
        "db": {
            "table": "hospital_intervencionquirurgica",
            "column": "external_id",
            "return": "id",
            "condition": True,
        },
    },
    # General
    {
        "field_id": 2,
        "name": "Sucursal",
        "type": str,
        "choices": None,
        "db": {
            "table": "transversal_ubicacion",
            "column": "descripcion",
            "return": "id",
            "condition": True,
        },
    },
    {
        "field_id": 3,
        "name": "Especialidad",
        "type": str,
        "choices": None,
        "db": {
            "table": "agenda_especialidad",
            "column": "nombre",
            "return": "id",
            "condition": True,
        },
    },
    {
        "field_id": 4,
        "name": "Profesional",
        "type": str,
        "choices": None,
        "db": {
            "table": "agenda_profesional",
            "column": "run",
            "return": "id",
            "condition": True,
        },
    },
    {"field_id": 6, "name": "Fecha", "type": "Date", "choices": None, "db": None},
    {"field_id": 7, "name": "Hora", "type": "Time", "choices": None, "db": None},
    {
        "field_id": 9,
        "name": "Paciente",
        "type": str,
        "choices": None,
        "db": {
            "table": "pacientes_paciente",
            "column": "run",
            "return": "id",
            "condition": True,
        },
    },
    {
        "field_id": 11,
        "name": "Usuario Creación",
        "type": str,
        "choices": None,
        "db": {
            "table": "auth_user",
            "column": "username",
            "return": "id",
            "condition": True,
        },
    },
    {
        "field_id": 23,
        "name": "Fecha Emisión",
        "type": "Date",
        "choices": None,
        "db": None,
    },
    # Citas
    {"field_id": 1, "name": "ID Cita", "type": str, "choices": None, "db": None},
    {
        "field_id": 5,
        "name": "Tipo de Cita",
        "type": str,
        "choices": None,
        "db": {
            "table": "agenda_tipocita",
            "column": "nombre",
            "return": "id",
            "condition": True,
        },
    },
    {"field_id": 8, "name": "Duración", "type": int, "choices": None, "db": None},
    {
        "field_id": 10,
        "name": "Estado Actual",
        "type": str,
        "choices": None,
        "db": {
            "table": "agenda_estado",
            "column": "nombre",
            "return": "id",
            "condition": True,
        },
    },
    {
        "field_id": 12,
        "name": "Observación Cita",
        "type": str,
        "choices": None,
        "db": None,
    },
    # Citas - Ambulatorio
    {
        "field_id": 13,
        "name": "Origen Cita",
        "type": "Time",
        "choices": None,
        "db": {
            "table": "agenda_citaorigen",
            "column": "nombre",
            "return": "id",
            "condition": True,
        },
    },
    {
        "field_id": 14,
        "name": "Campaña",
        "type": str,
        "choices": None,
        "db": {
            "table": "marketing_campania",
            "column": "nombre",
            "return": "id",
            "condition": True,
        },
    },
    # Citas - Examen
    {
        "field_id": 37,
        "name": "ID Grupo Exámen",
        "type": int,
        "choices": None,
        "db": None,
    },
    # Citas - Pabellón
    {
        "field_id": 38,
        "name": "Unidad",
        "type": str,
        "choices": None,
        "db": {
            "table": "hospital_unidad",
            "column": "nombre",
            "return": "id",
            "condition": True,
        },
    },
    {
        "field_id": 39,
        "name": "Presupuesto",
        "type": int,
        "choices": None,
        "db": None,
    },
    {
        "field_id": 40,
        "name": "Recurso",
        "type": str,
        "choices": None,
        "db": {
            "table": "agenda_recurso",
            "column": "nombre",
            "return": "id",
            "condition": True,
        },
    },
    # Registro Clinico
    {
        "field_id": 15,
        "name": "ID Registro Clinico",
        "type": str,
        "choices": None,
        "db": None,
    },
    {
        "field_id": 16,
        "name": "Fecha y Hora de Creación",
        "type": "DateTime",
        "choices": None,
        "db": None,
    },
    # Registro Clinico - Ambulatorio
    {
        "field_id": 17,
        "name": "Usuario Creador - Cierra Atención",
        "type": str,
        "choices": None,
        "db": {
            "table": "auth_user",
            "column": "username",
            "return": "id",
            "condition": True,
        },
    },
    {
        "field_id": 18,
        "name": "Nombre de Registro",
        "type": str,
        "choices": None,
        "db": None,
    },
    {
        "field_id": 19,
        "name": "Código Diagnóstico",
        "type": str,
        "choices": None,
        "db": {
            "table": "agenda_diagnosticoterminologia",
            "column": "codigo",
            "return": "id",
            "condition": True,
        },
    },
    {
        "field_id": 20,
        "name": "Estado Diagnóstico",
        "type": str,
        "choices": ESTADOS_DIAG,
        "db": None,
    },
    {
        "field_id": 21,
        "name": "Observación Diagnóstico",
        "type": str,
        "choices": None,
        "db": None,
    },
    # Registro Clínico - Hospitalizado
    {
        "field_id": 68,
        "name": "Tipo Registro",
        "type": str,
        "choices": TIPO_REGISTRO,
        "db": None,
    },
    {
        "field_id": 69,
        "name": "Nombre de Ficha",
        "type": str,
        "choices": None,
        "db": None,
    },
    # Recetas - Ambulatorias
    {"field_id": 22, "name": "ID Receta", "type": str, "choices": None, "db": None},
    {
        "field_id": 24,
        "name": "Código de Medicamento",
        "type": str,
        "choices": None,
        "db": {
            "table": "bodega_producto",
            "column": "codigo",
            "return": "id",
            "condition": True,
        },
    },
    {"field_id": 25, "name": "Dosis", "type": str, "choices": None, "db": None},
    {
        "field_id": 26,
        "name": "Tipo Dosis",
        "type": str,
        "choices": None,
        "db": {
            "table": "bodega_unidadmedida",
            "column": "nombre",
            "return": "id",
            "condition": True,
        },
    },
    {"field_id": 27, "name": "Frecuencia", "type": int, "choices": None, "db": None},
    {
        "field_id": 28,
        "name": "Tipo Frecuencia",
        "type": str,
        "choices": PERIODO_TIEMPO,
        "db": None,
    },
    {"field_id": 29, "name": "Período", "type": int, "choices": None, "db": None},
    {
        "field_id": 30,
        "name": "Tipo de Período",
        "type": str,
        "choices": None,
        "db": {
            "table": "bodega_tipoduracion",
            "column": "nombre",
            "return": "id",
            "condition": True,
        },
    },
    {
        "field_id": 31,
        "name": "Vía",
        "type": str,
        "choices": VIA,
        "db": None,
    },
    {"field_id": 32, "name": "Observaciones", "type": str, "choices": None, "db": None},
    # Órdenes de exámenes
    {
        "field_id": 33,
        "name": "ID Órden Exámen",
        "type": str,
        "choices": None,
        "db": None,
    },
    {
        "field_id": 34,
        "name": "Indicaciones",
        "type": str,
        "choices": None,
        "db": None,
    },
    {
        "field_id": 35,
        "name": "Diagnósticos",
        "type": str,
        "choices": None,
        "db": None,
    },
    {
        "field_id": 36,
        "name": "Exámen",
        "type": str,
        "choices": None,
        "db": {
            "table": "pacientes_examen",
            "column": "codigo",
            "return": "id",
            "condition": True,
        },
    },
    # Interconsultas
    {
        "field_id": 41,
        "name": "ID Derivación",
        "type": str,
        "choices": None,
        "db": None,
    },
    {
        "field_id": 42,
        "name": "Especialidad a Derivar",
        "type": str,
        "choices": None,
        "db": None,
    },
    {
        "field_id": 43,
        "name": "Que Se Desea Saber",
        "type": str,
        "choices": None,
        "db": None,
    },
    {
        "field_id": 44,
        "name": "Observación",
        "type": str,
        "choices": None,
        "db": None,
    },
    # Órden QX
    {
        "field_id": 45,
        "name": "ID Órden QX",
        "type": str,
        "choices": None,
        "db": None,
    },
    {
        "field_id": 46,
        "name": "Tipo Órden",
        "type": str,
        "choices": TIPO_ORDEN,
        "db": None,
    },
    {
        "field_id": 47,
        "name": "Cod. Cirugía",
        "type": str,
        "choices": None,
        "db": {
            "table": "recaudacion_prestacion",
            "column": "codigo",
            "return": "id",
            "condition": True,
        },
    },
    {
        "field_id": 48,
        "name": "Lateralidad",
        "type": str,
        "choices": None,
        "db": {
            "table": "hospital_lateralidad",
            "column": "nombre",
            "return": "id",
            "condition": True,
        },
    },
    {
        "field_id": 49,
        "name": "Pre-Requisitos",
        "type": str,
        "choices": None,
        "db": None,
    },
    # Tabla QX
    {
        "field_id": 50,
        "name": "ID Tabla QX",
        "type": str,
        "choices": None,
        "db": None,
    },
    {
        "field_id": 51,
        "name": "Observación Interna",
        "type": str,
        "choices": None,
        "db": None,
    },
    {
        "field_id": 52,
        "name": "Folio",
        "type": int,
        "choices": None,
        "db": None,
    },
    {
        "field_id": 53,
        "name": "Cirujano Principal",
        "type": str,
        "choices": None,
        "db": {
            "table": "agenda_profesional",
            "column": "run",
            "return": "id",
            "condition": True,
        },
    },
    {
        "field_id": 54,
        "name": "Anestesista",
        "type": str,
        "choices": None,
        "db": {
            "table": "agenda_profesional",
            "column": "run",
            "return": "id",
            "condition": True,
        },
    },
    {
        "field_id": 55,
        "name": "Ayudante",
        "type": str,
        "choices": None,
        "db": {
            "table": "agenda_profesional",
            "column": "run",
            "return": "id",
            "condition": True,
        },
    },
    {
        "field_id": 56,
        "name": "Estado QX",
        "type": str,
        "choices": None,
        "db": {
            "table": "hospital_estadohospitalizacion",
            "column": "nombre",
            "return": "id",
            "condition": True,
        },
    },
    {
        "field_id": 57,
        "name": "Estado Cuenta Médica",
        "type": str,
        "choices": None,
        "db": {
            "table": "hospital_estadocuentahospital",
            "column": "nombre",
            "return": "id",
            "condition": True,
        },
    },
    {
        "field_id": 58,
        "name": "RUT Prestador",
        "type": str,
        "choices": None,
        "db": {
            "table": "recaudacion_prestador",
            "column": "RUT",
            "return": "id",
            "condition": True,
        },
    },
    {
        "field_id": 59,
        "name": "Unidad",
        "type": str,
        "choices": None,
        "db": {
            "table": "hospital_unidad",
            "column": "nombre",
            "return": "id",
            "condition": True,
        },
    },
    {
        "field_id": 60,
        "name": "Recurso Pabellón",
        "type": str,
        "choices": None,
        "db": {
            "table": "agenda_recurso",
            "column": "nombre",
            "return": "id",
            "condition": True,
        },
    },
    # Presupuesto QX
    {
        "field_id": 61,
        "name": "ID Presupuesto",
        "type": str,
        "choices": None,
        "db": None,
    },
    {
        "field_id": 62,
        "name": "Nombre de Presupuesto",
        "type": str,
        "choices": None,
        "db": None,
    },
    {
        "field_id": 63,
        "name": "Estado Presupuesto",
        "type": str,
        "choices": None,
        "db": {
            "table": "hospital_estadopresupuesto",
            "column": "nombre",
            "return": "id",
            "condition": True,
        },
    },
    {
        "field_id": 64,
        "name": "Modalidad Presupuesto",
        "type": str,
        "choices": None,
        "db": {
            "table": "transversal_modalidad",
            "column": "nombre",
            "return": "id",
            "condition": True,
        },
    },
    {
        "field_id": 65,
        "name": "Código Prestación",
        "type": str,
        "choices": None,
        "db": {
            "table": "recaudacion_prestacion",
            "column": "codigo",
            "return": "id",
            "condition": True,
        },
    },
    {
        "field_id": 66,
        "name": "Cantidad",
        "type": int,
        "choices": None,
        "db": None,
    },
    {
        "field_id": 67,
        "name": "Precio",
        "type": int,
        "choices": None,
        "db": None,
    },
]

FORMATS = [
    {"format_id": 1, "description": "RUN Format"},
]

RESTRICTIONS = [
    # Custom
    {
        "restriction_id": 1,
        "description": "El campo debe estar entre un rango de 0 a 60",
        "regular_expression": "",
    },
]

if MOCKUP_CLIENT["use_case"] == 1:
    from config_ambulatorio import *
elif MOCKUP_CLIENT["use_case"] == 2:
    from config_pabellon import *
elif MOCKUP_CLIENT["use_case"] == 6:
    from config_examen import *
