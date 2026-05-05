# Limpieza de campos string — proyectos_data.json

## Objetivo

Limpiar los campos string de `proyectos_data.json` (v4) que venían con problemas desde la API fuente, generando un archivo limpio `proyectos_data_clean.json`.

	## Problemas detectados

| Campo | Espacios al final | Tildes | Newlines `\n` |
|---|---:|---:|---:|
| `origen.oficina` / `destino.oficina` | 44,985 de 45,030 | 1,355 | 0 |
| `origen.nombre` / `destino.nombre` | 0 | 209 | 0 |
| `proveidos[]` | 0 | 2,399 | 68 |
| `documento_desc` | 1,917 | 3,401 | 2,318 |

Las `oficinas` venían paddeadas a 500 caracteres con espacios.

## Solución aplicada

Script `limpiar_json.py` en la raíz del proyecto. Función de limpieza aplicada a todos los campos de texto:

```python
def limpiar(s):
    if not s:
        return s
    s = s.strip()                          # quita espacios al inicio y final
    s = s.replace('\n', ' ').replace('\r', ' ')  # newlines → espacio
    s = unicodedata.normalize('NFD', s)    # descompone caracteres acentuados
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')  # quita tildes
    return s
```

Campos limpiados: `oficina`, `nombre`, `proveidos`, `documento_desc`.  
Campos no tocados: `tipo_movimiento`, `fecha_mov`, `fecha_registro`, `documento_cud` — ya limpios o datos estructurados.

## Resultado

- Input: `proyectos_data.json` (original intacto)
- Output: `proyectos_data_clean.json` (archivo limpio)

Ejemplo antes/después:

| Campo | Antes | Después |
|---|---|---|
| `oficina` | `"GERENCIA REGIONAL DE INFRAESTRUCTURA` + 464 espacios`"` | `"GERENCIA REGIONAL DE INFRAESTRUCTURA"` |
| `documento_desc` | `"SOLICITO EVALUACIÓN DE...\nIMPACTO AMBIENTAL"` | `"SOLICITO EVALUACION DE... IMPACTO AMBIENTAL"` |
