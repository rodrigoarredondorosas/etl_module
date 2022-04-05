import petl as etl

from config import ID_MEDINET


def process_request(parameters):
    if parameters["step"] == 1:
        citas(parameters)
    elif parameters["step"] == 3:
        registro_clinico(parameters)
    elif parameters["step"] == 4:
        recetas(parameters)
    elif parameters["step"] == 5:
        orden_examen(parameters)
    elif parameters["step"] == 6:
        interconsultas(parameters)
    elif parameters["step"] == 7:
        orden_quirurgica(parameters)
    elif parameters["step"] == 8:
        tabla_quirurgica(parameters)
    elif parameters["step"] == 9:
        presupuesto_quirurgico(parameters)

    return "Proceso de carga terminado"


def clean_none(value):
    if value is None:
        return "NULL"
    else:
        return value


def validate_external_id(cursor, schema, table, id):
    query = f"SELECT id from {schema}.{table} where external_id = {id}"

    cursor.execute(query)

    response = cursor.fetchone()

    if response is None:
        return None
    else:
        response = response[0]
        return response


def get_db_value(cursor, schema, table, value, return_value):

    response = None

    query = f"SELECT {return_value} as value FROM {schema}.{table} WHERE id = {value}"

    cursor.execute(query)

    result = cursor.fetchone()

    if result[0]:
        response = result[0]

    return response


def citas(parameters):
    schema = parameters["schema"]
    cursor = parameters["cursor"]
    tipo_agenda = parameters["use_case"]

    for row in etl.dicts(parameters["data"]):
        try:
            fecha = row["Fecha"]  # Fecha
            hora = row["Hora"]  # Hora
            duracion = row["Duración"]  # Duracion
            estado = row[f"Estado Actual {ID_MEDINET}"]  # Estado Actual Medinet
            id_cita = row[f"ID Cita"]  # ID Cita
            paciente = row[f"Paciente {ID_MEDINET}"]  # Paciente Medinet
            sucursal = row[f"Sucursal {ID_MEDINET}"]  # Sucursal Medinet
            usuario = row[f"Usuario Creación {ID_MEDINET}"]  # Usuario Creación Medinet
            tipo_cita = row[f"Tipo de Cita {ID_MEDINET}"]  # Tipo de Cita Medinet

            chk_external_id = validate_external_id(
                cursor, schema, "agenda_cita", id_cita
            )

            if chk_external_id is not None:
                print(f"Cita : {id_cita} -> Registro ya existe en la base de datos ")
            else:
                # Insert into agenda_cita
                query_agenda_cita = f"""INSERT INTO {schema}.agenda_cita 
                (
                    fecha, 
                    hora, 
                    es_cancelada, 
                    created, 
                    modified, 
                    paciente_id, 
                    ubicacion_id, 
                    usuario_id, 
                    tipoagenda_id, 
                    estado_actual_id, 
                    confirmed_from, 
                    scheduled_from, 
                    encuenta_satisfaccion,
                    es_pagada_web, 
                    bono_visto, 
                    external_id,
                    duracion,
                    tipo_id
                    ) 
                VALUES
                (
                    {fecha},
                    {hora},
                    FALSE,
                    CURRENT_TIMESTAMP,
                    CURRENT_TIMESTAMP,
                    {paciente},
                    {sucursal},
                    {usuario},
                    {tipo_agenda},
                    {estado},
                    1,
                    1,
                    FALSE,
                    FALSE,
                    FALSE,
                    {id_cita},
                    {duracion},
                    {tipo_cita}
                )
                returning id;"""

                cursor.execute(query_agenda_cita)

                id = cursor.fetchone()
                agenda_cita_id = id[0]

                if tipo_agenda == 1:
                    # Ambulatorio
                    especialidad = row[
                        f"Especialidad {ID_MEDINET}"
                    ]  # Especialidad Medinet
                    profesional = row[
                        f"Profesional {ID_MEDINET}"
                    ]  # Profesional Medinet
                    campania = row[f"Campaña {ID_MEDINET}"]  # Campaña Medinet
                    origen_cita = row[f"Origen Cita {ID_MEDINET}"]
                    observaciones = row[f"Observación Cita"]  # Observación Cita

                    # Non required fields
                    campania = clean_none(campania)
                    observaciones = clean_none(observaciones)
                    origen_cita = clean_none(origen_cita)

                    query_update_agenda_cita = f""" UPDATE {schema}.agenda_cita 
                    SET 
                    especialidad_id = {especialidad},
                    profesional_id = {profesional},
                    campania_id = {campania}, 
                    origen_id = {origen_cita} 
                    where id = {agenda_cita_id}"""

                elif tipo_agenda == 2:
                    # Pabellón
                    observaciones = row[f"Observación Cita"]  # Observación Cita
                    presupuesto = row[f"Presupuesto"]  # Presupuesto
                    unidad = row[f"Unidad {ID_MEDINET}"]  # Unidad
                    recurso = row[f"Recurso {ID_MEDINET}"]  # Recurso

                    # Non required fields
                    observaciones = clean_none(observaciones)
                    presupuesto = clean_none(presupuesto)

                    query_update_agenda_cita = f""" UPDATE {schema}.agenda_cita 
                    SET 
                    unidad_id = {unidad}, 
                    recurso_id = {recurso} 
                    where id = {agenda_cita_id}"""

                elif tipo_agenda == 6:
                    # Exámen
                    especialidad = row[
                        f"Especialidad {ID_MEDINET}"
                    ]  # Especialidad Medinet
                    profesional = row[
                        f"Profesional {ID_MEDINET}"
                    ]  # Profesional Medinet
                    examen = row[f"Exámen {ID_MEDINET}"]  # Exámen ID Medinet
                    id_grupo_examen = row["ID Grupo Exámen"]  # ID Grupo Exámen
                    observaciones = "'Carga de Citas de Exámen'"

                    query_update_agenda_cita = f""" UPDATE {schema}.agenda_cita 
                    SET 
                    especialidad_id = {especialidad},
                    profesional_id = {profesional},
                    examen_id = {examen}, 
                    exam_group_id = {id_grupo_examen} 
                    where id = {agenda_cita_id}"""

                cursor.execute(query_update_agenda_cita)

                # Insert into agenda_historial
                query_agenda_historial = f"""INSERT INTO {schema}.agenda_historial
                (
                    observacion, 
                    fecha, 
                    cita_id,
                    estado_id
                ) 
                VALUES
                (
                    {observaciones},
                    CURRENT_TIMESTAMP,
                    {agenda_cita_id}, 
                    {estado}
                );"""

                cursor.execute(query_agenda_historial)

                print(f"Cita : {id_cita} -> Registro ingresado en la base de datos ")

        except Exception as error:
            print("An exception has occured:", error)
            print("Exception TYPE:", type(error))


def registro_clinico(parameters):
    schema = parameters["schema"]
    cursor = parameters["cursor"]

    for row in etl.dicts(parameters["data"]):
        try:
            # Params
            id_registro = row["ID Registro Clinico"]  # ID Registro Clinico
            fecha = row["Fecha y Hora de Creación"]  # Fecha y Hora de Creación

            if parameters["use_case"] == 1:
                usuario = row[
                    f"Usuario Creador - Cierra Atención {ID_MEDINET}"
                ]  # Usuario Creador - Cierra Atención Medinet
                id_cita = row[f"ID Cita {ID_MEDINET}"]  # ID Cita Medinet
                nombre_registro = row["Nombre de Registro"]  # Nombre de Registro
                json = "{}"

                # Non required fields

                # Validation
                query_paciente = (
                    f"SELECT paciente_id FROM {schema}.agenda_cita WHERE id = {id_cita}"
                )

                cursor.execute(query_paciente)

                paciente = cursor.fetchone()

                if paciente != None:
                    paciente = paciente[0]
                else:
                    print("Error al buscar paciente en la cita")
                    continue

                chk_external_id = validate_external_id(
                    cursor, schema, "pacientes_registro", id_registro
                )

                if chk_external_id is not None:
                    pacientes_registro_id = chk_external_id
                    msg = f"Registro Clínico : {id_registro} -> Registro ya existe en la base de datos"
                else:
                    # Insert into pacientes_registro
                    query_pacientes_registro = f"""INSERT INTO {schema}.pacientes_registro 
                    (
                        created, 
                        modified, 
                        paciente_id, 
                        usuario_id, 
                        odontogram,
                        es_pausado,
                        data,
                        arquetipo_id,
                        external_id,
                        nombre_registro
                    ) 
                    VALUES
                    (
                        {fecha},
                        CURRENT_TIMESTAMP,
                        {paciente},
                        {usuario},
                        '{json}',
                        false,
                        NULL,
                        NULL,
                        {id_registro},
                        {nombre_registro}
                    )
                    returning id;"""

                    cursor.execute(query_pacientes_registro)

                    id = cursor.fetchone()
                    pacientes_registro_id = id[0]

                    msg = f"Registro Clínico : {id_registro} -> Registro ingresado en la base de datos"

                    # Insert into agenda_cita_registros
                    query_agenda_cita_registros = f"""INSERT INTO {schema}.agenda_cita_registros 
                    (
                        cita_id,
                        registro_id
                    ) 
                    VALUES
                    (
                        {id_cita},
                        {pacientes_registro_id}
                    );"""

                    cursor.execute(query_agenda_cita_registros)

                # Diagnosticos

                diagnostico = row[
                    f"Código Diagnóstico {ID_MEDINET}"
                ]  # Código Diagnóstico ID MEDINET

                if diagnostico != "NULL":
                    estado_diagnostico = row[
                        f"Estado Diagnóstico {ID_MEDINET}"
                    ]  # Estado Diagnóstico
                    observacion_diagnostico = row[
                        "Observación Diagnóstico"
                    ]  # Observación Diagnósito

                    estado_diagnostico = clean_none(estado_diagnostico)
                    observacion_diagnostico = clean_none(observacion_diagnostico)

                    query_diagnostico = f"""INSERT INTO {schema}.pacientes_diagnosticoatencion
                    (
                        paciente_id,
                        cita_id,
                        diagnostico_id,
                        created,
                        created_by_id,
                        modified,
                        observacion,
                        estado
                    )
                    VALUES
                    (  
                        {paciente},
                        {id_cita},
                        {diagnostico},
                        {fecha},
                        {usuario},
                        CURRENT_TIMESTAMP,
                        {observacion_diagnostico},
                        {estado_diagnostico}
                    )"""

                    cursor.execute(query_diagnostico)
            elif parameters["use_case"] == 2:
                # ID Tabla QX ID MEDINET
                id_tabla = row[f"ID Tabla QX {ID_MEDINET}"]
                # ID Órden QX ID MEDINET
                id_orden = row[f"ID Órden QX {ID_MEDINET}"]
                # Usuario Creación ID MEDINET
                usuario = row[f"Usuario Creación {ID_MEDINET}"]
                # Paciente ID MEDINET
                paciente = row[f"Paciente {ID_MEDINET}"]
                # Tipo Registro
                tipo_registro = row[f"Tipo Registro {ID_MEDINET}"]
                # Nombre de Ficha
                nombre_ficha = row[f"Nombre de Ficha"]

                chk_external_id = validate_external_id(
                    cursor, schema, "hospital_registroclinico", id_registro
                )

                if chk_external_id is not None:
                    pacientes_registro_id = chk_external_id
                    msg = f"Registro Clínico : {id_registro} -> Registro ya existe en la base de datos"
                else:
                    query_pacientes_registro = f"""INSERT INTO {schema}.hospital_registroclinico
                        (
                            intervencion_id,
                            orden_id,
                            external_id,
                            arquetipo_id,
                            created,
                            modified,
                            created_by_id

                        ) 
                        VALUES
                        (
                            {id_tabla},
                            {id_orden},
                            {id_registro},
                            NULL,
                            {fecha},
                            CURRENT_TIMESTAMP,
                            {usuario}

                        )
                        returning id;"""

                    # print(query_pacientes_registro)

                    cursor.execute(query_pacientes_registro)

                    msg = f"Registro Clínico : {id_registro} -> Registro ingresado en la base de datos"

            print(msg)

        except Exception as error:
            print("An exception has occured:", error)
            print("Exception TYPE:", type(error))


def recetas(parameters):
    schema = parameters["schema"]
    cursor = parameters["cursor"]

    for row in etl.dicts(parameters["data"]):
        try:
            ESTADO = 1  # 1 Vigente 2 Cancelada
            id_receta = row["ID Receta"]  # ID Receta
            fecha = row["Fecha Emisión"]  # Fecha Emisión
            id_cita = row[f"ID Cita {ID_MEDINET}"]  # ID Cita FK Medinet
            paciente = row[f"Paciente {ID_MEDINET}"]  # Paciente Medinet
            profesional = row[f"Profesional {ID_MEDINET}"]  # Profesional Medinet
            producto_id = row[
                f"Código de Medicamento {ID_MEDINET}"
            ]  # Codigo de Medicamento Medinet
            dosis = row["Dosis"]  # Dosis
            dosis_tipo = row[f"Tipo Dosis {ID_MEDINET}"]  # Dosis Tipo Medinet
            intervalo = row["Frecuencia"]  # Frecuencia
            intervalo_tipo = row[
                f"Tipo Frecuencia {ID_MEDINET}"
            ]  # Tipo Frecuencia Medinet
            duracion = row["Período"]  # Período
            duracion_tipo = row[
                f"Tipo de Período {ID_MEDINET}"
            ]  # Tipo de Período Medinet
            via = row[f"Vía {ID_MEDINET}"]  # Vía Medinet
            observacion = row["Observaciones"]  # Observaciones

            # Non required fields
            paciente = clean_none(paciente)
            producto_id = clean_none(producto_id)
            dosis = clean_none(dosis)
            dosis_tipo = clean_none(dosis_tipo)
            duracion_tipo = clean_none(duracion_tipo)
            observacion = clean_none(observacion)

            chk_external_id = validate_external_id(
                cursor, schema, "pacientes_recetaambulatoria ", id_receta
            )

            if chk_external_id is not None:
                pacientes_recetaambulatoria_id = chk_external_id
                msg = f"Receta : {id_receta} -> Registro ya existe en la base de datos "
            else:
                # Insert into pacientes_recetaambulatoria
                query_pacientes_recetaambulatoria = f"""INSERT INTO {schema}.pacientes_recetaambulatoria 
                (
                    estado, 
                    created, 
                    modified, 
                    cita_id, 
                    paciente_id, 
                    profesional_id,
                    external_id
                ) 
                VALUES
                (
                    {ESTADO},
                    {fecha},
                    CURRENT_TIMESTAMP,
                    {id_cita},
                    {paciente},
                    {profesional},
                    {id_receta}
                )
                returning id;"""

                cursor.execute(query_pacientes_recetaambulatoria)

                id = cursor.fetchone()
                pacientes_recetaambulatoria_id = id[0]

                msg = f"Receta : {id_receta} -> Registro ingresado en la base de datos "

            # Insert into pacientes_recetaambulatoriaitem
            query_pacientes_recetaambulatoriaitem = f"""INSERT INTO {schema}.pacientes_recetaambulatoriaitem 
            (
                producto_id,
                dosis,
                dosis_tipo_id,
                intervalo,
                intervalo_tipo,
                duracion,
                duracion_tipo_id,
                via,
                observacion, 
                receta_id 
            ) 
            VALUES
            (
                {producto_id},
                {dosis},
                {dosis_tipo},
                {intervalo},
                {intervalo_tipo},
                {duracion},
                {duracion_tipo},
                {via},
                {observacion},
                {pacientes_recetaambulatoria_id}
            );"""

            cursor.execute(query_pacientes_recetaambulatoriaitem)

            print(msg)

        except Exception as error:
            print("An exception has occured:", error)
            print("Exception TYPE:", type(error))


def orden_examen(parameters):
    schema = parameters["schema"]
    cursor = parameters["cursor"]

    for row in etl.dicts(parameters["data"]):
        try:
            id_orden = row["ID Órden Exámen"]  # ID Órden Exámen
            id_registro_clinico = row[
                f"ID Registro Clínico {ID_MEDINET}"
            ]  # ID Registro Clínico Medinet
            id_cita = row[f"ID Cita {ID_MEDINET}"]  # ID Cita Medinet
            profesional = row[f"Profesional {ID_MEDINET}"]  # Profesional ID MEDINET
            paciente = row[f"Paciente {ID_MEDINET}"]  # Paciente ID MEDINET
            fecha_emision = row["Fecha Emisión"]  # Fecha Emisión
            indicaciones = row["Indicaciones"]  # Indicaciones
            diagnosticos = row["Diagnósticos"]  # Diagnósticos
            examen = row[f"Exámen {ID_MEDINET}"]  # Códigos de Exámen ID MEDINET

            # Default Values (cop)
            user = 133

            # Non required fields
            indicaciones = clean_none(indicaciones)
            diagnosticos = clean_none(diagnosticos)
            fecha_emision = clean_none(fecha_emision)

            chk_external_id = validate_external_id(
                cursor, schema, "pacientes_ordenmedica ", id_orden
            )

            if chk_external_id is not None:
                pacientes_ordenmedica_id = chk_external_id
                msg = f"Órden : {id_orden} -> Registro ya existe en la base de datos "
            else:
                query_orden_medica = f"""INSERT INTO {schema}.pacientes_ordenmedica 
                (
                    external_id,
                    cita_id,
                    paciente_id,
                    diagnosticos,
                    indicaciones,
                    created_by_id,
                    created) 
                VALUES(
                    {id_orden},
                    {id_cita},
                    {paciente},
                    {diagnosticos},
                    {indicaciones},
                    {user},
                    {fecha_emision})
                returning id;"""

                cursor.execute(query_orden_medica)

                id = cursor.fetchone()
                pacientes_ordenmedica_id = id[0]

                msg = f"Órden : {id_orden} -> Registro ingresado en la base de datos "

            query_orden_examen = f"""INSERT INTO {schema}.pacientes_ordenexamen 
            (
                orden_id,
                examen_id,
                diagnostico,
                indicaciones,
                es_entregado
                ,es_realizado
                ) VALUES(
                    {pacientes_ordenmedica_id},
                    {examen},
                    {diagnosticos},
                    {indicaciones},
                    false,
                    false);"""

            cursor.execute(query_orden_examen)

            print(msg)

        except Exception as error:
            print("An exception has occured:", error)
            print("Exception TYPE:", type(error))


def interconsultas(parameters):
    schema = parameters["schema"]
    cursor = parameters["cursor"]

    for row in etl.dicts(parameters["data"]):
        try:
            id_interconsulta = row["ID Derivación"]  # ID Derivación
            id_registro = row[
                f"ID Registro Clínico {ID_MEDINET}"
            ]  # ID Registro Clínico ID MEDINET
            id_cita = row[f"ID Cita {ID_MEDINET}"]  # ID Cita ID MEDINET
            observacion = row["Observación"]  # Observación
            fecha = row["Fecha Emisión"]  # Fecha Emisión
            paciente = row[f"Paciente {ID_MEDINET}"]  # Paciente
            profesional = row[f"Paciente {ID_MEDINET}"]  # Profesional
            especialidad = row["Especialidad a Derivar"]  # Especialidad a Derivar
            informacion_requerida = row["Que Se Desea Saber"]  # Que Se Desea Saber

            # Default Values (cop)
            user = 133
            sucursal = 1

            # Non required fields
            observacion = clean_none(observacion)
            fecha = clean_none(fecha)
            paciente = clean_none(paciente)
            informacion_requerida = clean_none(informacion_requerida)

            query_interconsulta = f"""INSERT INTO {schema}.pacientes_ordenexterna
            (
                especialidad_a_derivar,
                observacion,
                sintomatologia,
                informacion_requerida,
                created,modified,
                created_by_id,
                modified_by_id,
                paciente_id,
                ubicacion_id) 
                
                VALUES
            (
                {especialidad},
                {observacion},
                '',
                {informacion_requerida},
                {fecha},
                CURRENT_TIMESTAMP,
                {user},
                {user},
                {paciente},
                {sucursal});"""

            cursor.execute(query_interconsulta)

            print(
                f"Interconsulta : {id_interconsulta} -> Registro ingresado en la base de datos "
            )

        except Exception as error:
            print("An exception has occured:", error)
            print("Exception TYPE:", type(error))


def orden_quirurgica(parameters):
    schema = parameters["schema"]
    cursor = parameters["cursor"]

    for row in etl.dicts(parameters["data"]):
        try:
            id_orden = row[f"ID Órden QX"]  # ID Órden QX
            is_external = row[f"Tipo Órden {ID_MEDINET}"]  # Tipo Órden ID MEDINET
            prestacion = row[f"Cod. Cirugía {ID_MEDINET}"]  # Cod. Cirugía ID MEDINET
            lateralidad = row[f"Lateralidad {ID_MEDINET}"]  # Lateralidad ID MEDINET
            paciente = row[f"Paciente {ID_MEDINET}"]  # Paciente ID MEDINET
            profesional = row[f"Profesional {ID_MEDINET}"]  # Profesional ID MEDINET
            pre_requisitos = row[f"Pre-Requisitos"]  # Pre-Requisitos
            fecha_emision = row[f"Fecha Emisión"]  # Fecha Emisión
            observaciones = row[f"Observación"]  # Observación
            id_cita = row[f"ID Cita {ID_MEDINET}"]  # ID Cita ID MEDINET
            prevision_id = None

            # Validation
            query_paciente = f"SELECT prevision_id FROM {schema}.pacientes_paciente WHERE id = {paciente}"

            cursor.execute(query_paciente)

            prevision_paciente = cursor.fetchone()

            if prevision_paciente != None:
                prevision_id = prevision_paciente[0]
            else:
                print("Error al buscar la previsión del paciente")
                continue

            # Default Values (cop)
            especialidad = 1
            sucursal = 1
            duracion_estimada = 60
            estado = 1
            tipo = 2

            # Non required fields
            pre_requisitos = clean_none(pre_requisitos)
            observaciones = clean_none(observaciones)

            chk_external_id = validate_external_id(
                cursor, schema, "hospital_ordenquirurgica ", id_orden
            )

            if chk_external_id is not None:
                hospital_ordenquirurgica_id = chk_external_id
                msg = (
                    f"Órden QX : {id_orden} -> Registro ya existe en la base de datos "
                )
            else:
                query_orden_quirurgica = f"""INSERT INTO {schema}.hospital_ordenquirurgica 
                (
                    external_id,
                    requerimientos, 
                    duracion_estimada, 
                    created,
                    modified,
                    especialidad_id, 
                    estado_id, 
                    paciente_id, 
                    prevision_id,
                    profesional_id,
                    ubicacion_id, 
                    is_external,
                    type,
                    observacion,
                    cita_id) 
                VALUES(
                    {id_orden},
                    {pre_requisitos},
                    60,
                    {fecha_emision},
                    CURRENT_TIMESTAMP,
                    {especialidad},
                    {estado},
                    {paciente},
                    {prevision_id},
                    {profesional},
                    {sucursal},
                    {is_external},
                    {tipo},
                    {observaciones},
                    {id_cita})
                returning id;
                """

                cursor.execute(query_orden_quirurgica)

                id = cursor.fetchone()
                hospital_ordenquirurgica_id = id[0]

                msg = f"Órden : {id_orden} -> Registro ingresado en la base de datos "

            query_item_quirurgico = f"""INSERT INTO {schema}.hospital_itemquirurgico 
            (
                cargar_paquetizados, 
                lateralidad_id, 
                orden_id, 
                prestacion_id) 
            VALUES
            (
                FALSE,
                {lateralidad},
                {hospital_ordenquirurgica_id},
                {prestacion});
            """

            cursor.execute(query_item_quirurgico)

            print(msg)
        except Exception as error:
            print("An exception has occured:", error)
            print("Exception TYPE:", type(error))


def tabla_quirurgica(parameters):
    schema = parameters["schema"]
    cursor = parameters["cursor"]

    for row in etl.dicts(parameters["data"]):
        try:
            id_tabla = row["ID Tabla QX"]  # ID Tabla QX
            id_cita = row[f"ID Cita {ID_MEDINET}"]  # ID Cita ID MEDINET
            usuario = row[
                f"Usuario Creación {ID_MEDINET}"
            ]  # Usuario Creación ID MEDINET
            fecha = row["Fecha y Hora de Creación"]  # Fecha y Hora de Creación
            paciente = row[f"Paciente {ID_MEDINET}"]  # Paciente ID MEDINET
            observacion = row[f"Observación Interna"]  # Observación Interna
            id_orden_qx = row[f"ID Órden QX {ID_MEDINET}"]  # Orden QX ID MEDINET
            folio = row["Folio"]  # Folio
            cirujano = row[
                f"Cirujano Principal {ID_MEDINET}"
            ]  # Cirujano Principal ID MEDINET
            anestesista = row[f"Anestesista {ID_MEDINET}"]  # Anestesista ID MEDINET
            ayudante = row[f"Ayudante {ID_MEDINET}"]  # Ayudante ID MEDINET
            estado = row[f"Estado QX {ID_MEDINET}"]  # Estado QX ID MEDINET
            estado_cuenta = row[
                f"Estado Cuenta Médica {ID_MEDINET}"
            ]  # Estado Cuenta Médica
            prestador = row[f"RUT Prestador {ID_MEDINET}"]  # RUT Prestador ID MEDINET
            unidad = row[f"Unidad {ID_MEDINET}"]  # Unidad ID MEDINET
            recurso = row[
                f"Recurso Pabellón {ID_MEDINET}"
            ]  # Recurso Pabellón ID MEDINET

            prevision_id = get_db_value(
                cursor, schema, "pacientes_paciente", paciente, "prevision_id"
            )

            if prevision_id == None:
                print("Error al buscar la previsión del paciente")
                continue

            # Non required fields
            fecha = clean_none(fecha)
            observacion = clean_none(observacion)
            folio = clean_none(folio)

            # Default Values (cop)
            especialidad = 1
            sucursal = 1
            modalidad = 1
            estado_qx = 1

            chk_external_id = validate_external_id(
                cursor, schema, "hospital_intervencionquirurgica ", id_tabla
            )

            if chk_external_id is not None:
                hospital_intervencionquirurgica_id = chk_external_id
                msg = (
                    f"Tabla QX : {id_tabla} -> Registro ya existe en la base de datos "
                )
            else:
                query_tabla_quirurgica = f"""INSERT INTO {schema}.hospital_intervencionquirurgica 
                (
                    orden_id, 
                    estado_id, 
                    cita_id, 
                    observacion, 
                    created, 
                    modified,
                    external_id   
                )
                values
                (
                    {id_orden_qx}, 
                    {estado_qx}, 
                    {id_cita}, 
                    {observacion}, 
                    {fecha}, 
                    CURRENT_TIMESTAMP,
                    {id_tabla}   
                ) returning id;"""

                cursor.execute(query_tabla_quirurgica)

                id = cursor.fetchone()

                hospital_intervencionquirurgica_id = id[0]

                msg = f"Tabla : {id_tabla} -> Registro ingresado en la base de datos "

                query_hospitalizacion = f"""INSERT INTO {schema}.hospital_hospitalizacion
                (
                    observacion,
                    fecha_ingreso, 
                    created, 
                    modified, 
                    paciente_id, 
                    prevision_id, 
                    especialidad_id, 
                    modalidad, 
                    ubicacion_id, 
                    estado_id, 
                    motivo_alta, 
                    unidad_al_egreso_id            
                ) 
                VALUES
                (
                    '',
                    {fecha},
                    {fecha},
                    CURRENT_TIMESTAMP,
                    {paciente},
                    {prevision_id},
                    {especialidad},
                    {modalidad},
                    {sucursal},
                    {estado},
                    '',
                    {unidad}          
                ) returning id;
                """

                cursor.execute(query_hospitalizacion)

                id = cursor.fetchone()

                hospital_hospitalizacion_id = id[0]

                query_intervencionquirurgica_hospitalizacion = f"""INSERT INTO {schema}.hospital_intervencionquirurgica_hospitalizacion(
                    intervencionquirurgica_id,
                    hospitalizacion_id) 
                VALUES(
                    {hospital_intervencionquirurgica_id},
                    {hospital_hospitalizacion_id});
                """

                cursor.execute(query_intervencionquirurgica_hospitalizacion)

                query_cuenta_hospital = f"""INSERT INTO {schema}.hospital_cuentahospital 
                (
                    hospitalizacion_id,
                    prestador_id,
                    folio,
                    estado_id,
                    cuenta_cerrada
                )
                VALUES
                (
                    {hospital_hospitalizacion_id},
                    {prestador},
                    {folio},
                    {estado_cuenta},
                    FALSE
                )"""

                cursor.execute(query_cuenta_hospital)

                query_hospital_equipoqx = f"""INSERT INTO {schema}.hospital_equipoqx 
                (
                    orden_id, 
                    nombre , 
                    created, 
                    created_by_id , 
                    modified)
                VALUES 
                (
                    {id_orden_qx},
                    '',
                    {fecha},
                    {usuario},
                    CURRENT_TIMESTAMP
                ) returning id"""

                cursor.execute(query_hospital_equipoqx)

                id = cursor.fetchone()

                hospital_equipoqx_id = id[0]

                query_hospital_integranteequipoqx_cirujano = f"""INSERT INTO {schema}.hospital_integranteequipoqx 
                (
                    equipoqx_id,
                    funcion_id,
                    profesional_id,
                    is_present_in_surgery
                )
                VALUES
                (
                    {hospital_equipoqx_id},
                    2,
                    {cirujano},
                    FALSE
                )"""

                cursor.execute(query_hospital_integranteequipoqx_cirujano)

                query_hospital_integranteequipoqx_anestesista = f"""INSERT INTO {schema}.hospital_integranteequipoqx 
                    (
                        equipoqx_id,
                        funcion_id,
                        profesional_id,
                        is_present_in_surgery
                    )
                    VALUES
                    (
                        {hospital_equipoqx_id},
                        3,
                        {anestesista},
                        FALSE
                    )"""

                cursor.execute(query_hospital_integranteequipoqx_anestesista)

                query_hospital_integranteequipoqx_ayudante = f"""INSERT INTO {schema}.hospital_integranteequipoqx 
                    (
                        equipoqx_id,
                        funcion_id,
                        profesional_id,
                        is_present_in_surgery
                    )
                    VALUES
                    (
                        {hospital_equipoqx_id},
                        15,
                        {ayudante},
                        FALSE
                    )"""

                cursor.execute(query_hospital_integranteequipoqx_ayudante)

                msg = (
                    f"Tabla Quirúrgica: {id_tabla} -> Registro ingresado con éxito"
                )

            print(msg)

        except Exception as error:
            print("An exception has occured:", error)
            print("Exception TYPE:", type(error))


def presupuesto_quirurgico(parameters):
    schema = parameters["schema"]
    cursor = parameters["cursor"]

    for row in etl.dicts(parameters["data"]):
        try:
            id_presupuesto = row["ID Presupuesto"]  # ID Presupuesto
            id_orden_qx = row[f"ID Órden QX {ID_MEDINET}"]  # ID Órden QX ID MEDINET
            usuario = row[
                f"Usuario Creación {ID_MEDINET}"
            ]  # Usuario Creación ID MEDINET
            fecha = row["Fecha y Hora de Creación"]  # Fecha y Hora de Creación
            paciente = row[f"Paciente {ID_MEDINET}"]  # Paciente
            nombre_presupuesto = row[f"Nombre de Presupuesto"]  # Nombre de Presupuesto
            ubicacion = row[f"Sucursal {ID_MEDINET}"]  # Sucursal ID MEDINET
            estado = row[f"Estado Presupuesto {ID_MEDINET}"]  # Estado Presupuesto ID MEDINET
            modalidad = row[
                f"Modalidad Presupuesto {ID_MEDINET}"
            ]  # Modalidad Presupuesto ID MEDINET
            prestador = row[f"RUT Prestador {ID_MEDINET}"]  # RUT Prestador ID MEDINET
            prestacion = row[f"Código Prestación {ID_MEDINET}"]  # Código Prestación ID MEDINET
            cantidad = row["Cantidad"]  # Cantidad
            precio = row["Precio"]  # Precio
            lateralidad = row[f"Lateralidad {ID_MEDINET}"] # Lateralidad ID MEDINET

            prevision_id = None

            # Validation
            query_paciente = f"SELECT prevision_id FROM {schema}.pacientes_paciente WHERE id = {paciente}"

            cursor.execute(query_paciente)

            prevision_paciente = cursor.fetchone()

            if prevision_paciente != None:
                prevision_id = prevision_paciente[0]
            else:
                print("Error al buscar la previsión del paciente")
                continue

            # Non required fields
            nombre_presupuesto = clean_none(nombre_presupuesto)
            fecha = clean_none(fecha)

            chk_external_id = validate_external_id(
                cursor, schema, "hospital_presupuestoquirurgico", id_presupuesto
            )

            if chk_external_id is not None:
                hospital_presupuestoquirurgico_id = chk_external_id
                msg = (
                    f"Presupuesto QX: {id_presupuesto} -> Registro ya existe en la base de datos "
                )
            else:
                query_presupuesto_quirurgico = f"""INSERT INTO {schema}.hospital_presupuestoquirurgico 
                (
                    orden_id,
                    ubicacion_id,
                    nombre,
                    estado_id,
                    created,
                    created_by_id,
                    modified,
                    modified_by_id,
                    lateralidad_id,
                    es_activo,
                    external_id
                )
                values
                (
                    {id_orden_qx},
                    {ubicacion},
                    {nombre_presupuesto},
                    {estado},
                    {fecha},
                    {usuario},
                    CURRENT_TIMESTAMP,
                    {usuario},
                    {lateralidad},
                    TRUE,
                    {id_presupuesto}
                ) returning id"""

                cursor.execute(query_presupuesto_quirurgico)

                id = cursor.fetchone()

                hospital_presupuestoquirurgico_id = id[0]

                msg = (
                    f"Presupuesto QX: {id_presupuesto} -> Registro ingresado con éxito"
                )
            
            query_presupuesto_quirurgico_prestacion = f"""INSERT INTO {schema}.hospital_presupuestoquirurgicoprestacion 
            (
                created, 
                modified, 
                prestacion_id, 
                prestador_id, 
                presupuesto_id,
                modalidad_id,
                modalidad_padre_id) 
            VALUES(
                {fecha},
                CURRENT_TIMESTAMP,
                {prestacion},
                {prestador},
                {hospital_presupuestoquirurgico_id},
                {prevision_id},
                {modalidad})
            returning id;"""

            cursor.execute(query_presupuesto_quirurgico_prestacion)

            id = cursor.fetchone()

            hospital_presupuestoquirurgicoprestacion_id = id[0]

            query_presupuesto_quirurgico_item = f"""INSERT INTO {schema}.hospital_presupuestoquirurgicoitem 
            (
                created, 
                modified, 
                prestacion_id, 
                presupuesto_id,
                presupuesto_cirugia_id,
                cantidad,
                precio_unitario,
                descuento )
            VALUES(
                {fecha},
                CURRENT_TIMESTAMP,
                {prestacion},
                {hospital_presupuestoquirurgico_id},
                {hospital_presupuestoquirurgicoprestacion_id},
                {cantidad},
                {precio},
                0);
            """

            cursor.execute(query_presupuesto_quirurgico_item)

            print(msg)

        except Exception as error:
            print("An exception has occured:", error)
            print("Exception TYPE:", type(error))
