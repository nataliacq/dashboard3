# Exploración del JSON — Hallazgos del chat

## Estructura del JSON v4 (`proyectos_data.json`)

El archivo `proyectos_data.json` usa una estructura diferente a la v3. Los campos de las transacciones cambian:

```
transacciones[]
├── transac_id          : number
├── tipo_movimiento     : string   — texto legible: "GENERADO", "DERIVADO", "RECIBIDO", "ADJUNTADO", ...
├── fecha_mov           : string   — "DD/MM/YYYY HH:MM:SS"
├── origen
│   ├── nombre          : string
│   └── oficina         : string   (con espacios al final)
├── destino
│   ├── nombre          : string
│   └── oficina         : string   (con espacios al final)
└── proveidos           : Array<string>   — instrucciones/notas al recibir o derivar
```

`documentos_hijos` tiene estructura plana (sin wrapper `documento_principal`):
```
documentos_hijos[]
├── documento_id
├── documento_cud
├── documento_desc
├── fecha_registro
└── transacciones[]
```

---

## Hallazgos

### `proveidos` con tipo_movimiento "RECIBIDO"
- **285 casos** con `tipo_movimiento == "RECIBIDO"` y `proveidos` no vacío.
- El contenido tiene formato: `"Proveído/Observación: <texto>"` (encoding roto en la fuente: `í` → `\xed`).
- Ejemplos: `"EMITIR OPINION EN EL DIA"`, `"urgente"`, `"SE REMITE VISADO - ADJ. PROYECTO DE OFICIO"`.

### `proveidos` con múltiples valores
- `proveidos` es un **array de strings**, no un string con comas.
- Casos con más de un elemento siempre tienen los mismos 3 valores predefinidos:
  ```
  ["ATENCION", "CONOCIMIENTO Y FINES", "TRAMITE CORRESPONDIENTE"]
  ```
- Todos son de tipo `DERIVADO` (no `RECIBIDO`).

### Jerarquía de documentos
- **Ningún documento hijo tiene hijos propios** — la jerarquía es máximo 2 niveles (padre → hijo).

### CUDs con "informe técnico" → Subgerencia de Formulación y Evaluación de Inversiones
- **32 CUDs** encontrados con descripción relacionada a "informe técnico" y con al menos una transacción con destino a esa oficina.
- Mayoría corresponde al flujo de solicitud de Informe Previo a la Contraloría (Ley N° 29230).
- Nota: el nombre de la oficina en el JSON tiene encoding roto (`ó` → `\xf3`), hay que buscar por substring `"formulaci"`.

### Código de movimiento `ADJUNTADO`
- Existe el tipo `ADJUNTADO` — no estaba documentado en el catálogo original.
- Ejemplo: `transac_id 10039262` → CUD `20250011142069`, CUI `2509546`, fecha `20/05/2025 14:12:01`.
- La transacción **no contiene un puntero directo** al documento padre al que se adjunta.

### ¿Cómo encontrar el padre de un `ADJUNTADO`?
Dos enfoques posibles:
1. Buscar el CUD del hijo en el array `documentos_hijos` de todos los documentos del dataset.
2. Buscar el `documento_id` numérico del hijo referenciado en otros documentos.

Limitación: si el padre pertenece a un CUI no descargado, no aparecerá en el dataset local.

---

## Análisis temporal: diferencia entre `ADJUNTADO` del hijo y `GENERADO` del padre

Sobre **470 pares únicos** padre-hijo con ambas fechas presentes:

| Métrica | Valor |
|---|---|
| Mínima diferencia | 0 segundos |
| Mediana | 1.4 minutos |
| Máxima diferencia | ~15 días (21,739 min) |
| **> 1 hora** | **187 casos (39.8%)** |
| **> 1 día** | **68 casos (14.5%)** |

**Conclusión:** la ventana temporal no es un criterio confiable para identificar al padre de un documento `ADJUNTADO`. Casi 4 de cada 10 pares superan 1 hora de diferencia y 1 de cada 7 supera el día.
