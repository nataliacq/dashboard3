● json_loader.py encapsula el acceso a proyectos_data_clean.json en tres capas:

  1. Carga
  - cargar_datos() — lee el JSON y retorna el dict crudo. Usa el path del archivo por defecto, no
   hace falta pasarlo.

  2. Búsqueda puntual (retorna el objeto completo con documento_principal + documentos_hijos)
  - buscar_por_documento_id(data, 2388754) — busca por ID numérico interno
  - buscar_por_cud(data, "20260011129573") — busca por código único de documento

  3. DataFrames (para análisis, filtros, agrupaciones con pandas)
  - df_documentos(data) — una fila por documento; columnas: CUI, IDs, descripción, fecha,
  cantidad de transacciones e hijospuedo
  - df_transacciones(data) — una fila por movimiento; columnas: quién derivó a quién, desde qué
  oficina, cuándo, con qué proveído
  - df_hijos(data) — una fila por documento hijo; incluye referencia al padre

  Las fechas (fecha_registro, fecha_mov) se convierten automáticamente a datetime64 para poder
  filtrar por rango sin conversión adicional.

✻ Crunched for 8s

❯ osea puedo llamar solo a df_transacciones sin llamar a las otras funciones si importo          
  json-loader-module                                                                             
                                                                                                 
● Sí, exacto. Cada función es independiente, solo necesitas cargar_datos() primero porque todas  
  reciben data como parámetro:                 
                                                                                                 
  from json_loader import cargar_datos, df_transacciones
                                                                                                 
  data = cargar_datos()                                           
  trans = df_transacciones(data)

  cargar_datos() es el único paso obligatorio — es quien lee el archivo. Las tres funciones de
  DataFrame (df_documentos, df_transacciones, df_hijos) y las dos de búsqueda son completamente
  independientes entre sí.