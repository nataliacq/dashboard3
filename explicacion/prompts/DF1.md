- prompt
    - input: dataClean4.json y considera estructura json descrita en estructuraJSONnuevo.md
    - objetivo:
        - generar z4mapDF1.py en directorio preprocessing que genere dataframe con todos los datos de transacciones ordenadas por movimientos del documento.
        - esta programa sera llamado luego por otro.
    - definicion "movimiento":
        - es el desplazamiento de documento de oficina a otra, equivale a tipo_movimiento de derivacion + recepcion.
        - si varias transacciones de tipo derivacion estan dentro de un "movimiento" si se realizan exactamente al mismo tiempo
    - output: dataframe con columnas :
        1. CUI
        2. codigo_mov : codigo numerico autogenerado de un movimiento
        3. documento_desc: descripcion del documento
        4. fecha_derivado: fecha y hora en que se derivo
        5. fecha_recibido: fecha y hora en que se recibio
        6. documento_cud
        7. origen: Persona/oficina que ejecuta la acción
        8. destino: Persona/oficina que recibe
        9. adjunto
    - **pasos para armar tabla en dataframe:** por cada root key (CUI), en cada documento_principal y sus documentos_hijos, identificar "movimientos" en el arreglo "transacciones" asi :
        - agrupa las transacciones por "movimiento":
            - 1. buscar transacciones que deben ser agrupadas:
                - condicion: "tipo_movimiento": "DERIVADO" , mismo valor de fecha_mov y mismo origen (oficina y nombre).
                - estas pertenecen a un movimiento. entonces tienen mismo codigo_mov
            - 2. buscar el par de cada transaccion encontrada en el paso anterior asi:
                - condicion: "tipo_movimiento": "RECIBIDO", mismo destino(oficina y nombre) y mismo origen (oficina y nombre)
            - 3. se genera una fila por cada par de transacciones con las columnas:
                - cada agrupacion de transacciones "movimiento" tendrá los mismos valores en las columnas:
                    - CUI, documento_cud, codigo_mov (autogenerar), documento_desc, origen (columnas origen_oficina y origen_nombre), fecha_derivado (fecha_mov repetida), adjunto (lista de documento_desc de documentos_hijos)
                - en cada fila se escriben datos complementarios que salen en el par encontrado en el paso 2: fecha_recibido, destino (columnas destino_oficina y destino_nombre), transac_id_recepcion (transac_id)
            - 4. agrega columnas "adjCUD" donde van los CUD de los documentos_hijos separado por ";" y columna "adjDocDesc" con los valores de "documento_desc" de los hijos separados por ";"
    - luego de armar dataframe:
	    - antes de hacer "return dataframe" exportado en csv en directorio "data" con el nombre de dataframe. si ya existe archivo con ese nombre colocarle dataframe2, si ya existe entonces dataframe3 y asi consecutivamente.