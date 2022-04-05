import re
import petl as etl
import psycopg2 as db_utils
import xlsxwriter
from openpyxl import Workbook
from config import (
    USE_CASES,
    FIELDS,
    STEPS,
    FORMATS,
    RELATION_FIELDS_FORMATS,
    RELATION,
    RELATION_FIELDS_RESTRICTIONS,
    RESTRICTIONS,
    ID_MEDINET,
)
from datetime import datetime, time


def look(table):
    print(etl.look(table))


# Getters
def get_active_relation(client, relations):
    active_relation = None

    for relation in relations:
        if client["use_case"] == relation["use_case"]:
            active_relation = relation
    return active_relation


def get_active_relation_data(r_id, step, relations_fields):
    active_relation_data = None

    for relation_data in relations_fields:
        if r_id == relation_data["r_id"] and step == relation_data["step_id"]:
            active_relation_data = relation_data

    return active_relation_data


def get_usecase_data(num):
    global USE_CASES
    active_use_case = None
    for use_case in USE_CASES:
        if use_case["u_id"] == num:
            active_use_case = use_case
    return active_use_case


def get_field_data(num):
    global FIELDS
    active_field = None
    for field in FIELDS:
        if field["field_id"] == num:
            active_field = field
    return active_field


def get_step_data(num):
    global STEPS
    active_step = None
    for step in STEPS:
        if step["step_id"] == num:
            active_step = step
    return active_step


def get_restrictions(rf_id, field):
    global RELATION_FIELDS_RESTRICTIONS

    restrictions = None

    for relation_restrictions in RELATION_FIELDS_RESTRICTIONS:
        if (
            rf_id in relation_restrictions["rf_id"]
            and relation_restrictions["field"] == field
        ):
            restrictions = relation_restrictions["restrictions"]

    return restrictions


def get_restriction_data(num):
    global RESTRICTIONS
    active_restriction = None
    for restriction in RESTRICTIONS:
        if restriction["restriction_id"] == num:
            active_restriction = restriction
    return active_restriction


def get_formats(rf_id, field):
    global RELATION_FIELDS_FORMATS

    formats = None

    for relation_formats in RELATION_FIELDS_FORMATS:
        if rf_id in relation_formats["rf_id"] and relation_formats["field"] == field:
            formats = relation_formats["formats"]

    return formats


# Validate Columns
def validate_columns(data, relation_data):
    status = True
    text = ""

    field_names = etl.fieldnames(data)

    for field in relation_data["fields"]:
        field_data = get_field_data(field)
        if field_data["name"] not in field_names:
            status = False
            text += "* Non existing field -> " + field_data["name"]

    response = {"status": status, "description": text}
    return response


# Clean Data
def clean_data(data, relation_data):
    data = etl.addfield(data, "Validation Status", True)
    data = etl.addfield(data, "Validation Description", "")
    rf_id = relation_data["rf_id"]
    for field in relation_data["fields"]:
        field_data = get_field_data(field)
        field_name = field_data["name"]
        field_type = field_data["type"]
        # Convert
        data = converter(data, field_name, field_type)
        # Required Fields
        if field in relation_data["required_fields"]:
            data = validate_required_fields(data, field_name)
        # Required Relation Fields
        if relation_data["required_relation_fields"] != None:
            for required_relation_fields in relation_data["required_relation_fields"]:
                if field == required_relation_fields["if"]:
                    data = validate_relation_required_fields(
                        data, field_name, required_relation_fields["then"]
                    )
        # Restrictions
        restrictions = get_restrictions(rf_id, field)
        if restrictions != None:
            for restriction_id in restrictions:
                data = restriction(data, field_name, restriction_id)
        # Formats
        formats = get_formats(rf_id, field)
        if formats != None:
            for format_id in formats:
                data = formatter(data, field_name, format_id)

    return data


def converter(data, field_name, field_type):
    if field_type in [int, "Date", "Time", "DateTime"]:
        if field_type is int:
            data = etl.convert(
                data, field_name, lambda x: None if x is None else int(x)
            )
            msg = "numérico"
            where_convert = lambda y: y[field_name] == None
        else:
            if field_type == "Date":
                msg = "DD-MM-YYYY o YYYY-MM-DD"
            elif field_type == "Time":
                msg = "HH:MM:SS"
            elif field_type == "DateTime":
                msg = "DD-MM-YYYY HH:MM:SS o YYYY-MM-DD HH:MM:SS"

            where_convert = (
                lambda y: validate_datetime(y[field_name], field_type) == False
            )

        data = etl.convert(
            data,
            {
                "Validation Status": lambda x: False,
                "Validation Description": lambda x: str(x)
                + "\n"
                + f"* {field_name} -> Debe ser campo {msg}",
            },
            where=where_convert,
        )
    elif field_type is str:
        data = etl.convert(
            data, field_name, lambda x: None if x is None else f"{str(x).strip()}"
        )

    return data


def validate_datetime(value, field_type):
    validation = False

    if value == None:
        return True

    try:
        if field_type in ["DateTime", "Date"] and type(value) == datetime:
            validation = True
        elif field_type == "Time" and type(value) == time:
            validation = True
    except:
        return validation

    return validation


def validate_required_fields(data, field_name):
    validation_description = f"* Campo Obligatorio -> {field_name} "

    data = etl.convert(
        data,
        {
            "Validation Status": lambda x: False,
            "Validation Description": lambda x: str(x) + "\n" + validation_description,
        },
        where=lambda y: y[field_name] == None,
    )

    return data


def validate_relation_required_fields(data, field_name, required_fields):

    for field in required_fields:
        field_data = get_field_data(field)

        validation_description = (
            f"* Campo Obligatorio -> {field_data['name']} si se ingresa {field_name}"
        )

        data = etl.convert(
            data,
            {
                "Validation Status": lambda x: False,
                "Validation Description": lambda x: str(x)
                + "\n"
                + validation_description,
            },
            where=lambda y: y[field_name] != None and y[field_data["name"]] == None,
        )

    return data


def restriction(data, field_name, restriction_id):
    active_restriction = get_restriction_data(restriction_id)
    restriction_description = active_restriction["description"]
    validation_description = f"* {field_name} -> {restriction_description} "

    data = etl.convert(
        data,
        {
            "Validation Status": lambda x: False,
            "Validation Description": lambda x: str(x) + "\n" + validation_description,
        },
        where=lambda y: restriction_handler(y[field_name], active_restriction) == False,
    )

    return data


def restriction_handler(value, restriction):
    if value is None:
        return True

    status = False

    try:
        if restriction["restriction_id"] == 1:
            if 0 <= value <= 60:
                status = True
    except:
        status = False

    return status


def formatter(data, field_name, format_id):
    data = etl.convert(
        data,
        field_name,
        lambda x: format_handler(x, format_id),
        where=lambda y: y["Validation Status"] == True,
    )

    return data


def format_handler(value, format_id):
    if value == None:
        pass
    elif format_id == 1:
        # RUN
        return value  # Se deshabilita temporalmente
        value = str(value)
        value = value.replace(".", "")
        value = value.replace("-", "")
        for i, c in enumerate(reversed(value)):
            if i == 0:
                value = "-%s" % c
            elif i in (3, 6, 9):
                value = ".%s%s" % (c, value)
            else:
                value = "%s%s" % (c, value)

    return value


# Map Data
def map_data(data, relation_data, schema):
    rf_id = relation_data["rf_id"]
    for field in relation_data["fields"]:
        field_data = get_field_data(field)
        required = False

        if field in relation_data["required_fields"]:
            required = True
            
        if field_data["db"] != None:
            data = mapper(
                data,
                field_data["name"],
                field_data["db"],
                schema,
                "db",
                required,
            )
        elif field_data["choices"] != None:
            data = mapper(
                data,
                field_data["name"],
                field_data["choices"],
                schema,
                "choices",
                required,
            )
    return data


def mapper(data, field_name, parameters, schema, call, required):
    global ID_MEDINET
    if call == "choices":
        catalogs = parameters
        error_msg = (
            f"* {field_name} -> El valor no fue encontrado en la constante {catalogs}"
        )
    elif call == "db":
        table = parameters["table"]
        column = parameters["column"]
        return_value = parameters["return"]

        connection = open_connection()

        cursor = connection.cursor()

        query_catalog = f'SELECT distinct({return_value}) as id, "{column}" as column FROM {schema}.{table} WHERE "{column}" is not null'

        cursor.execute(query_catalog)

        catalogs = None

        catalogs = cursor.fetchall()

        error_msg = f"* {field_name} -> El valor no fue encontrado en la columna {column} de la tabla {table}"

    data = etl.addfield(
        data,
        f"{field_name} {ID_MEDINET}",
        lambda x: map_handler(x[field_name], catalogs, required),
    )

    data = etl.convert(
        data,
        {
            "Validation Status": lambda x: False,
            "Validation Description": lambda x: str(x) + "\n" + error_msg,
        },
        where=lambda y: y[f"{field_name} {ID_MEDINET}"] == None,
    )

    return data


def map_handler(value, catalogs, required):
    mapped_value = None

    for catalog in catalogs:
        if str(value) == str(catalog[1]):
            mapped_value = catalog[0]

    if value == None and required == False:
        # if value is empty and not required can be null
        mapped_value = "NULL"

    return mapped_value


# Prepare Data
def prepare_data(data, relation_data):
    for field in relation_data["fields"]:
        field_data = get_field_data(field)
        field_name = field_data["name"]
        field_type = field_data["type"]

        if field_type in [str, "Date", "DateTime", "Time"]:
            data = etl.convert(
                data, field_name, lambda x: None if x is None else f"'{x}'"
            )

    return data


# Connection
def open_connection():
    connection = db_utils.connect(
        host="localhost",
        database="medinet_testing3",
        user="postgres",
        password="seis123",
        port="5432",
    )

    return connection


# Excel
def print_excel(client, relations, relations_fields):
    active_step = get_step_data(client["step"])
    excel_name = active_step["excel_name"].lower()

    workbook = xlsxwriter.Workbook(f"excel_{excel_name}.xlsx")

    active_relation = get_active_relation(client, relations)

    cont = 0
    active_relation_data = get_active_relation_data(
        active_relation["r_id"],
        client["step"],
        relations_fields,
    )

    active_use_case = get_usecase_data(client["use_case"])
    worksheet = workbook.add_worksheet(active_use_case["name"])
    excel_fields = active_relation_data["fields"]
    for field in excel_fields:
        field_data = get_field_data(field)
        cell_format = workbook.add_format()
        if field in active_relation_data["foreign_keys"]:
            cell_format.set_bold()
            cell_format.set_font_color("blue")
        elif field in active_relation_data["required_fields"]:
            cell_format.set_bold()
            cell_format.set_font_color("red")
        worksheet.write(0, cont, field_data["name"], cell_format)
        cont += 1
    workbook.close()
