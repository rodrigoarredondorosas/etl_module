Archivos
===========
 -  main.py -> ejecuta el flujo de prefect (extract , transform y load)
 -  utils.py -> contiene toda la lógica de las funciones que se utilizan en el archivo main.py
 -  request.py -> recibe la petición desde el archivo main.py para cargar los datos en la base de datos
 -  config.py -> archivo de configuración general que contiene la configuración de las variables USE_CASES, STEPS, FIELDS, MOCKUP_CLIENT, RESTRICTIONS, FORMATS
  - config_ambulatorio.py -> archivo de configuración para el caso de uso ambulatorio (1).
  - config_pabellon.py -> archivo de configuración para el caso de uso quirúrgico (2).
  - config_examen -> archivo de configuración para el caso de uso exámen (6)
  * contienen la configuración de RELATION , RELATION_FIELDS , RELATION_FIELDS_FORMATS, RELATION_FIELDS_RESTRICTION


Como utilizar el proyecto
=========================

Antes de comenzar a configurar las variables, instalar las dependencias del archivo requirements.txt

1. Configurar la variable MOCKUP_CLIENT con el use_case, step, schema y excel a ejecutar.

Por ejemplo para configurar las citas de ambulatorio sería

.. code-block:: python

    MOCKUP_CLIENT = {
        "use_case": 1,
        "step": 1,
        "schema": "schema156294258446voxxxm",
        "document": "excel_citas.xlsx",
    }

Además configurar la conexión a la base de datos, para esto revisar utils.py open_connection

.. code-block:: python

    def open_connection():
        connection = db_utils.connect(
            host="localhost",
            database="medinet_testing3",
            user="postgres",
            password="seis123",
            port="5432",
        )

2. Si el excel ingresado en MOCKUP_CLIENT["document"] no existe, ejecutar el archivo print_excel.py para crearlo.

3. Ejecutar el archivo main.py
    - extract_from_xlsx -> extraerá los datos del archivo excel
    - get_relation_data -> cargará la configuración del archivo config_ambulatorio/config_pabellon/config_examen dependiendo del use_case y step de MOCKUP_CLIENT.
    - transform 
        -> Valida que el excel no esté vacío
        -> Valida que las columnas del excel sean las mismas que las columnas configuradas en los archivos de config_ambulatorio/config_pabellon/config_examen (revisar utils.py validate_columns)
        -> Valida que la data cumpla con el formato solicitado (revisar utils.py clean_data)
        -> Valida que la data exista en la base de datos para campos correspondientes a catalogos (revisar utils.py map_data)
        -> Prepara la data para la inserción a la base de datos (revisar utils.py prepare_data_to_sql)
   - load -> envía petición al archivo request.py con los siguientes parametros
