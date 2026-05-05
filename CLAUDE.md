# Instrucciones — Trazabilidad OXI Dashboard

## Entorno Python

- Ejecutar Python con `py` (no `python`)
- `openpyxl` está instalada para leer Excel
- Si el archivo `.xlsm` está abierto en Excel, copiarlo a `%TEMP%` antes de leerlo con openpyxl
- Para importar módulos de `preprocessing/` usar `sys.path.insert(0, 'preprocessing')`

## Convenciones de código

- Todos los archivos JSON se leen/escriben con `encoding="utf-8"`, `ensure_ascii=False`, `indent=2`
- Las funciones de transformación en `limpiar_json2.py` deben tener firma `(dict) -> tuple[dict, dict]` para ser compatibles con `aplicar_filtros()`
