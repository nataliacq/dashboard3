# json_loader.py — Módulo de acceso al JSON

## Contexto

`proyectos_data_clean.json` es un dict donde la clave es el CUI y el valor es una lista de documentos. Acceder a campos anidados como `documento_id` o `documentos_hijos` requería iterar manualmente. `json_loader.py` encapsula esa lógica.

---

## Por qué existía el problema de búsqueda

En el primer intento se usó `data.get('2388754')` asumiendo que las claves eran `documento_id`. Las claves reales son **CUI** (ej: `'2615250'`). El `documento_id` está anidado dentro de cada objeto de la lista. La corrección fue iterar sobre todos los CUI y sus listas para encontrar el campo interno.

---

## Funciones del módulo

### Carga
```python
cargar_datos(path=DEFAULT_PATH) -> dict
```
Lee el JSON. `DEFAULT_PATH` apunta al archivo en el mismo directorio que el módulo.

### Búsqueda puntual
```python
buscar_por_documento_id(data, 2388754)   # por ID numérico
buscar_por_cud(data, "20260011129573")   # por código único
```
Ambas retornan el objeto completo `{"documento_principal": ..., "documentos_hijos": [...]}` o `None`.

### DataFrames
```python
df_documentos(data)      # 1 fila por documento principal
df_transacciones(data)   # 1 fila por movimiento/transacción
df_hijos(data)           # 1 fila por documento hijo
```

---

## Columnas de cada DataFrame

### df_documentos
| Columna | Descripción |
|---|---|
| `cui` | Clave top-level del JSON |
| `documento_id` | ID interno del documento |
| `documento_cud` | Código único del documento |
| `documento_desc` | Asunto/descripción |
| `fecha_registro` | datetime64 |
| `num_transacciones` | Cantidad de movimientos |
| `num_hijos` | Cantidad de documentos hijos |

### df_transacciones
| Columna | Descripción |
|---|---|
| `cui` | CUI del proyecto |
| `documento_id` | ID del documento padre |
| `documento_cud` | CUD del documento padre |
| `transac_id` | ID de la transacción |
| `tipo_movimiento` | GENERADO, DERIVADO, RECIBIDO, etc. |
| `fecha_mov` | datetime64 |
| `origen_nombre` | Persona que ejecuta |
| `origen_oficina` | Oficina de origen |
| `destino_nombre` | Persona que recibe |
| `destino_oficina` | Oficina de destino |
| `proveidos` | Instrucciones (string, separadas por "; ") |

### df_hijos
| Columna | Descripción |
|---|---|
| `cui` | CUI del proyecto |
| `parent_documento_id` | ID del documento padre |
| `parent_documento_cud` | CUD del documento padre |
| `documento_id` | ID del hijo |
| `documento_cud` | CUD del hijo |
| `documento_desc` | Descripción del hijo |
| `fecha_registro` | datetime64 |
| `num_transacciones` | Transacciones del hijo |

---

## Volumen de datos (proyectos_data_clean.json actual)

| DataFrame | Filas | Columnas |
|---|---|---|
| df_documentos | 2 876 | 7 |
| df_transacciones | 10 485 | 11 |
| df_hijos | 1 866 | 8 |

---

## Uso básico

```python
from json_loader import cargar_datos, buscar_por_cud, df_transacciones

data = cargar_datos()

# Búsqueda puntual
obj = buscar_por_cud(data, "20260011129573")
print(len(obj["documentos_hijos"]))   # 1

# DataFrame de transacciones solamente
trans = df_transacciones(data)
trans[trans["tipo_movimiento"] == "DERIVADO"]
```

---

## Dict vs DataFrame

| Situación | Usar |
|---|---|
| Buscar un documento específico | dict (`buscar_por_*`) |
| Acceder a estructura completa con hijos | dict |
| Filtrar por fecha, oficina, tipo de movimiento | DataFrame |
| Agrupar, contar, cruzar datos | DataFrame |
| Exportar a Excel/CSV | DataFrame |

Las funciones son independientes entre sí. Solo `cargar_datos()` es obligatorio antes de cualquiera.
