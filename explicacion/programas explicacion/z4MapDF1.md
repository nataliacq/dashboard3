● Resultados
- 5,965 filas × 14 columnas — todas las columnas esperadas presentes.                                   
  - 512 filas sin par RECIBIDO — fecha_recibido = NaT y transac_id_recepcion = NaN, como corresponde a    
  derivaciones sin recepción aún.
  - codigo_mov llega a 5,088 movimientos únicos.                                                          
  - CSV exportado a data/dataframe.csv.                           
  - Filas 0 y 1 muestran exactamente el ejemplo del registro de muestra (CUI 2615250), con los movimientos
   y pares correctos.

  El archivo creado es preprocessing/z4mapDF1.py y expone generar_df1(data=None) -> pd.DataFrame.