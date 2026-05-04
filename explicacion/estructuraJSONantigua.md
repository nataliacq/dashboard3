# Estructura del archivo `cui_XXXXXXX.json`

El archivo es un **array** de objetos (uno por documento encontrado para ese CUI):

```
Array
└── [0], [1], ...  — cada elemento es un documento
    ├── documento_principal
    │   ├── documento_id      : number   — ID interno (ej: 2379916)
    │   ├── documento_cud     : string   — Código único (ej: "20260011120735")
    │   ├── documento_desc    : string   — Asunto/descripción del documento
    │   ├── fecha_registro    : null     — siempre null en los datos actuales
    │   └── transacciones     : Array
    │       └── [0], [1], ...  — cada movimiento del documento
    │           ├── transac_id      : number   — ID de la transacción
    │           ├── codigo          : string   — tipo de movimiento (GE/DE/RE/AR/AD/EX/CO/CC/D1/D2)
    │           ├── fecha_mov       : string   — "DD/MM/YYYY HH:MM:SS"
    │           ├── nombre_origen   : string   — persona que ejecuta la acción
    │           ├── oficina_origen  : string   — oficina de origen (con espacios al final)
    │           ├── nombre_destino  : string   — persona que recibe
    │           └── oficina_destino : string   — oficina de destino (con espacios al final)
    └── documentos_hijos      : Array   — siempre vacío []
```

---

## Notas importantes sobre los datos reales

| Observación | Detalle |
|---|---|
| **Duplicados** | Cada `transac_id` aparece hasta 4 veces seguidas. Deduplicar por `(transac_id, codigo)` |
| **Espacios** | `oficina_origen` y `oficina_destino` tienen ~500 caracteres de espacios al final — aplicar `.strip()` |
| **`fecha_registro`** | Siempre `null` |
| **`documentos_hijos`** | Siempre `[]` |

---

## Códigos de movimiento

| Código | Significado |
|---|---|
| `GE` | Generado / creado |
| `DE` | Derivado / enviado |
| `RE` | Recibido |
| `AR` | Archivado / cerrado |
| `AD` | Vinculado a respuesta posterior |
| `EX` | Derivado a externo |
| `CO` | Se deriva copia |
| `CC` | Se recibe copia |
| `D1` / `D2` | Devuelto |

### Flujo típico de un documento

`GE` → `DE` → `RE` → (trabajo interno con `DE`/`RE`) → `AR` o `AD`
