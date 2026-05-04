# Estructura de Transacciones — "REMITO DOCUMENTACION COMPLEMENTARIA" (Obras por Impuestos)

Documentos con `documento_desc` similar a:
> *REMITO DOCUMENTACION COMPLEMENTARIA RELACIONADA CON LA SOLICITUD DE EMISION DE INFORME PREVIO EN MATERIA DE OBRAS POR IMPUESTOS DEL PROYECTO DE INVERSION*

Se encontraron **8 documentos** en 5 CUIs distintos (3 de ellos tienen un duplicado sin transacciones relevantes).

---

## Patrón general (prácticamente idéntico en todos)

```
DERIVADO: TORRES ROBLEDO, LUIS RAMON (GOBERNACION REGIONAL)
       → TORRES ROBLEDO, LUIS RAMON (GOBERNACION REGIONAL)   ← se auto-deriva primero

DERIVADO: TORRES ROBLEDO, LUIS RAMON (GOBERNACION REGIONAL)
       → RAMOS ZAVALA, FREDDY FERNANDO (COMITE ESPECIAL LEY 29230)

RECIBIDO: RAMOS ZAVALA, FREDDY FERNANDO (COMITE ESPECIAL LEY 29230)

ARCHIVADO (en COMITE ESPECIAL LEY 29230)
```

---

## Detalle por CUI

| CUI | CUD | Fecha DERIVADO | Fecha ARCHIVADO | Destino final |
|-----|-----|---------------|-----------------|---------------|
| 2659383 | 20250011380383 | 23/12/2025 | 29/12/2025 | CARPIO CAMACHO, JAIME (GERENCIA GENERAL REGIONAL)* |
| 2195474 | 20260011051617 | 20/02/2026 | 13/04/2026 | RAMOS ZAVALA (COMITE ESPECIAL LEY 29230) |
| 2652607 | 20260011093458 | 27/03/2026 | 30/03/2026 | RAMOS ZAVALA (COMITE ESPECIAL LEY 29230) |
| 2654114 | 20260011081434 | 17/03/2026 | 30/03/2026 | RAMOS ZAVALA (COMITE ESPECIAL LEY 29230) |
| 2654115 | 20260011081446 | 17/03/2026 | 30/03/2026 | RAMOS ZAVALA (COMITE ESPECIAL LEY 29230) |

\*El CUI 2659383 es el único que difiere: después de derivar a RAMOS ZAVALA, hay un segundo DERIVADO+RECIBIDO hacia **CARPIO CAMACHO (GERENCIA GENERAL REGIONAL)**, y el ARCHIVADO queda en esa oficina.

---

## Observaciones

- Los CUIs 2652607, 2654114 y 2654115 tienen un segundo documento con el mismo asunto pero **sin transacciones** (CUDs: 20260011092231, 20260011079667, 20260011080492) — probablemente documentos duplicados/borradores.
- La auto-derivación `TORRES ROBLEDO → TORRES ROBLEDO` es un patrón recurrente, posiblemente para registrar la recepción del documento físico antes de derivarlo al comité.
- Tipos de movimiento excluidos del análisis: `GENERADO`, `ADJUNTADO`.
