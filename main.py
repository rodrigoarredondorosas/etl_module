import petl as etl
from prefect import task, Flow, Parameter
from config import (
    RELATION,
    MOCKUP_CLIENT,
    RELATION_FIELDS,
)
from utils import (
    look,
    get_active_relation,
    get_active_relation_data,
    validate_columns,
    get_usecase_data,
    clean_data,
    map_data,
    formatter,
    open_connection,
    prepare_data,
)

from request import process_request


@task
def extract_from_xlsx(path, use_case):
    data = None

    active_use_case = get_usecase_data(use_case)

    data = etl.fromxlsx(path, active_use_case["name"])

    return data


@task
def get_relation_data(MOCKUP_CLIENT, RELATION, RELATION_FIELDS):
    active_relation = get_active_relation(MOCKUP_CLIENT, RELATION)

    active_relation_data = get_active_relation_data(
        active_relation["r_id"],
        MOCKUP_CLIENT["step"],
        RELATION_FIELDS,
    )

    return active_relation_data


@task
def transform(data, relation_data, schema):
    try:
        # Validate Empty
        if data is None or not etl.nrows(data):
            print("Empty Data")
            return None

        # Validate Columns
        validator = validate_columns(data, relation_data)

        if validator["status"] is False:
            print(validator["description"])
            return None

        # Clean Data
        cleaned_data = clean_data(data, relation_data)

        rejected_cleaned_data = etl.selectis(cleaned_data, "Validation Status", False)
        print(
            f"Número de filas con errores de limpieza {etl.nrows(rejected_cleaned_data)}"
        )
        if etl.nrows(rejected_cleaned_data):
            print(rejected_cleaned_data)
        etl.toxlsx(rejected_cleaned_data, "excel_rejected_cleaned_data.xlsx")

        # Database Validation
        mapped_data = map_data(
            etl.selectis(cleaned_data, "Validation Status", True), relation_data, schema
        )

        rejected_mapped_data = etl.selectis(mapped_data, "Validation Status", False)
        print(f"Número de filas con errores de mapeo {etl.nrows(rejected_mapped_data)}")
        if etl.nrows(rejected_mapped_data):
            print(rejected_mapped_data)
        etl.toxlsx(rejected_mapped_data, "excel_rejected_mapped_data.xlsx")

        # Prepare Data to SQL
        data = prepare_data(
            etl.selectis(mapped_data, "Validation Status", True), relation_data
        )

        etl.toxlsx(data, "excel_data_to_sql.xlsx")

        return data
    except Exception as error:
        print("An exception has occured:", error)
        print("Exception TYPE:", type(error))


@task
def load(transformed_data, client):
    if transformed_data is None:
        print("Error ocurred processing the file, abort loading...")
    else:
        print("Loading Django Model...")

        connection = open_connection()

        cursor = connection.cursor()

        parameters = {
            "data": transformed_data,
            "schema": client["schema"],
            "cursor": cursor,
            "use_case": client["use_case"],
            "step": client["step"],
        }

        response = process_request(parameters)

        print(response)

        connection.commit()
        # connection.rollback()


def build_flow():

    with Flow("ETL_Module") as flow:
        # parameters
        path_to_xlsx = Parameter(name="path_to_xlsx", required=True)

        # extract
        data = extract_from_xlsx(path_to_xlsx, MOCKUP_CLIENT["use_case"])

        # config
        relation_data = get_relation_data(MOCKUP_CLIENT, RELATION, RELATION_FIELDS)

        # transform
        transformed_data = transform(data, relation_data, MOCKUP_CLIENT["schema"])

        # load
        load(transformed_data, MOCKUP_CLIENT)
    return flow


if __name__ == "__main__":
    path_to_xlsx = MOCKUP_CLIENT["document"]
    flow = build_flow()
    flow.run(parameters={"path_to_xlsx": path_to_xlsx})
