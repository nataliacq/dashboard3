# Estructura del JSON — `proyectos_data.json` (v4)

## Nivel raíz

```json
{
  "<CUI>": [ ... ]   // clave = número de CUI del proyecto; valor = array de documentos
}
```

## Documento (elemento del array por CUI)

```json
{
  "documento_principal": { ... },
  "documentos_hijos": [ ... ]
}
```

## `documento_principal`

| Campo            | Tipo                 | Descripción                                                                 |
| ---------------- | -------------------- | --------------------------------------------------------------------------- |
| `documento_id`   | `number`             | ID interno del documento                                                    |
| `documento_cud`  | `string`             | Código Único de Documento (ej: `"20260011129573"`)                          |
| `documento_desc` | `string`             | Asunto / descripción del documento                                          |
| `fecha_registro` | `string`             | Fecha y hora de registro `"DD/MM/YYYY HH:MM:SS"` (en v3 era siempre `null`) |
| `transacciones`  | `array<Transaccion>` | Historial de movimientos del documento                                      |

## `Transaccion`

| Campo             | Tipo            | Descripción                                                   |
| ----------------- | --------------- | ------------------------------------------------------------- |
| `transac_id`      | `number`        | ID único de la transacción                                    |
| `tipo_movimiento` | `string`        | Tipo de movimiento (ver tabla de valores abajo)               |
| `fecha_mov`       | `string`        | Fecha y hora `"DD/MM/YYYY HH:MM:SS"`                          |
| `origen`          | `Persona`       | Persona/oficina que ejecuta la acción                         |
| `destino`         | `Persona`       | Persona/oficina que recibe                                    |
| `proveidos`       | `array<string>` | Instrucciones/anotaciones del proveído (puede ser vacío `[]`) |

## `Persona` (objeto anidado en `origen` y `destino`)

| Campo     | Tipo     | Descripción                                                                     |
| --------- | -------- | ------------------------------------------------------------------------------- |
| `nombre`  | `string` | Nombre completo (formato `APELLIDO APELLIDO, NOMBRE`)                           |
| `oficina` | `string` | Nombre de la oficina — viene con espacios al final, usar `.strip()` al procesar |

## `documentos_hijos` (elemento del array)

Tiene la misma estructura que `documento_principal`: campos `documento_id`, `documento_cud`, `documento_desc`, `fecha_registro`, `transacciones`.

---
## Valores de `tipo_movimiento`

| Valor        | Equivalente v3 | Significado |
|--------------|:--------------:|-------------|
| `GENERADO`   | `GE`           | Documento creado en el sistema |
| `DERIVADO`   | `DE`           | Enviado / remitido a otra persona u oficina |
| `RECIBIDO`   | `RE`           | Recepción del documento derivado |
| `ADJUNTADO`  | `AD`           | Documento vinculado/adjuntado a otro (respuesta o expediente) |
| `ARCHIVADO`  | `AR`           | Cerrado / archivado sin nueva derivación activa |
| `DEVUELTO`   | `D1` / `D2`   | Documento derivado que es devuelto al remitente |

> **Nota:** En v4 el campo es texto completo (`tipo_movimiento`) en lugar del código corto (`codigo`) de v3. No se observaron equivalentes a `EX`, `CO` ni `CC` en el dataset actual.

---

## Observaciones importantes

- **Sin duplicados de transac_id:** a diferencia de v3, no se repiten transacciones; no es necesario deduplicar.
- **Espacios en `oficina`:** los nombres de oficina siguen viniendo con espacios al final — aplicar `.strip()`.
- **`proveidos`:** campo nuevo en v4; array de strings con instrucciones del proveído; frecuentemente vacío.
- **`fecha_registro` poblada:** en v3 siempre era `null`; en v4 contiene la fecha real de registro.
- **`documentos_hijos` no vacío:** en v4 puede contener documentos hijo con estructura completa.
