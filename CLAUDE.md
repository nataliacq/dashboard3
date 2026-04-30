# Contexto del Proyecto — Trazabilidad OXI Dashboard

## Rutas de archivos clave

- **JSONs descargados:** `C:\Users\HP\Documents\OneDrive\TRAZABILIDAD OXI DASHBOARD\json\v3\json_descargados\`
  - Formato de nombre: `cui_XXXXXXX.json`
- **Catálogo de códigos (Excel):** `C:\Users\HP\Documents\OneDrive\OXI ESTADO\OXI ESTADO.xlsm`
  - Hoja relevante: `QmqCod`

## Estructura del JSON (por CUI)

Cada archivo `cui_XXXXXXX.json` es un **array de objetos**, donde cada objeto representa un documento con su historial de movimientos.

```
[
  {
    "documento_principal": {
      "documento_id": number,        // ID interno del documento
      "documento_cud": string,       // Código Único de Documento (ej: "20260011120735")
      "documento_desc": string,      // Asunto / descripción del documento
      "fecha_registro": null | date, // Generalmente null
      "transacciones": [             // Historial de movimientos
        {
          "transac_id": number,      // ID de la transacción
          "codigo": string,          // Tipo de movimiento (ver catálogo abajo)
          "fecha_mov": string,       // Fecha y hora "DD/MM/YYYY HH:MM:SS"
          "nombre_origen": string,   // Persona que ejecuta la acción
          "oficina_origen": string,  // Oficina de origen (viene con espacios al final)
          "nombre_destino": string,  // Persona que recibe
          "oficina_destino": string  // Oficina de destino (viene con espacios al final)
        }
      ]
    },
    "documentos_hijos": []           // Siempre vacío en los archivos analizados
  }
]
```

### Observaciones importantes sobre los datos
- Las transacciones tienen **duplicados**: el mismo `transac_id` aparece varias veces (hasta 4x). Para análisis, deduplicar por `(transac_id, codigo)`.
- Los campos `oficina_origen` y `oficina_destino` tienen **espacios en blanco al final** — usar `.strip()` al procesar.
- `documentos_hijos` siempre es array vacío en los archivos actuales.
- `fecha_registro` siempre es `null`.

## Catálogo de códigos de movimiento (hoja QmqCod)

| Código | Significado |
|--------|-------------|
| `GE`   | Generado / documento creado |
| `DE`   | Derivado / enviado / remitido a otra persona u oficina |
| `RE`   | Recibido / recepción del documento derivado |
| `AD`   | Documento queda vinculado a una respuesta o documento posterior |
| `AR`   | Archivado / cerrado sin nueva derivación activa |
| `EX`   | Derivado a una persona externa a la organización |
| `CO`   | Se deriva Copia |
| `CC`   | Se recibe la Copia derivada a través de "CO" |
| `D1`   | Documento que fue derivado es devuelto |
| `D2`   | Documento que fue derivado es devuelto |

### Flujo típico de un documento
`GE` → `DE` → `RE` → (trabajo interno con `DE`/`RE`) → `AR` o `AD`

### Patrones observados
- **Fan-out:** un documento se deriva simultáneamente a varias oficinas (mismo timestamp, distintos `transac_id`)
- **Ida y vuelta:** documento circula entre personas de la misma oficina durante revisión

## Herramientas disponibles en este entorno

- **Python:** disponible como `py` (Python 3.13.5 en `C:\Users\HP\AppData\Local\Programs\Python\Python313\`)
- **Librería openpyxl:** instalada, para leer archivos Excel
- **Nota:** si el Excel está abierto en Excel, copiarlo primero a `%TEMP%` antes de leerlo con openpyxl

## Ejemplo de código Python para procesar un JSON

```python
import json

with open(r'C:\Users\HP\Documents\OneDrive\TRAZABILIDAD OXI DASHBOARD\json\v3\json_descargados\cui_2195474.json', encoding='utf-8') as f:
    data = json.load(f)

for obj in data:
    dp = obj['documento_principal']
    cud = dp['documento_cud']
    transacs = dp['transacciones']

    # Deduplicar por (transac_id, codigo)
    vistos = set()
    unicos = []
    for t in transacs:
        key = (t['transac_id'], t['codigo'])
        if key not in vistos:
            vistos.add(key)
            unicos.append(t)

    des = [t for t in unicos if t['codigo'] == 'DE']
    print(f"CUD {cud}: {len(des)} derivaciones únicas")
```
