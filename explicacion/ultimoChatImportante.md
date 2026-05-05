# Chat Importante - Dashboard3 Setup & Análisis JSON

## 1. Crear repositorio git

```bash
git init
```
Inicializado en `C:/Users/HP/PycharmProjects/dashboard3`.
Se renombró `.gitignore.txt` → `.gitignore` y se hizo el commit inicial.

---

## 2. Subir repo a GitHub

```bash
git remote add origin https://github.com/nataliacq/dashboard3.git
git push -u origin master
```
Repo publicado en: https://github.com/nataliacq/dashboard3

---

## 3. Script de descarga de API interna

**API:** `http://10.128.145.23/api-cui/api.php?cui=<CUI>`  
**Fuente de códigos:** `proyectosList` (35 proyectos)  
**Script:** `descargar_proyectos.py`

Lógica:
- Lee los CUIs de `proyectosList`
- Detecta automáticamente la última versión en `TRAZABILIDAD OXI DASHBOARD\json\` (v0, v1, v2, v3...)
- Crea la siguiente carpeta (ej. `v4`) y guarda `proyectos_data.json` ahí
- Delay de 200ms entre requests para no saturar la API

Resultado de ejecución: **35/35 exitosos**, guardado en `v4\proyectos_data.json`

---

## 4. Estructura del JSON (`proyectos_data.json`)

### Nivel raíz
```json
{
  "2615250": [ ... ],
  "2617569": [ ... ]
}
```
- Clave: **CUI del proyecto**
- Valor: **array de trámites** (un proyecto puede tener varios trámites activos)

---

### Cada elemento del array = un trámite
```json
{
  "documento_principal": { ... },
  "documentos_hijos": [ ... ]
}
```

---

### `documento_principal`
| Campo | Tipo | Descripción |
|---|---|---|
| `documento_id` | int | ID único interno |
| `documento_cud` | string | Código único del documento (ej. `"20260011129573"`) |
| `documento_desc` | string | Asunto/descripción del trámite |
| `fecha_registro` | string | Fecha y hora de registro |
| `transacciones` | array | Historial de movimientos entre oficinas |

---

### `transacciones` — recorrido del documento

Cada transacción representa un paso:

| `tipo_movimiento` | Significado |
|---|---|
| `GENERADO` | Creado por primera vez |
| `DERIVADO` | Enviado a otra persona/oficina |
| `RECIBIDO` | Confirmación de recepción |
| `ADJUNTADO` | Se adjuntó un documento hijo |

Campos por transacción:
- `transac_id`: int
- `tipo_movimiento`: string
- `fecha_mov`: string
- `origen`: `{ nombre, oficina }`
- `destino`: `{ nombre, oficina }`
- `proveidos`: array de strings con instrucciones (ej. `"TRAMITE CORRESPONDIENTE"`, `"ATENCION"`)

---

### `documentos_hijos`
Array de documentos con la misma estructura que `documento_principal`. Son documentos de respuesta, informes o adjuntos relacionados al trámite principal.

---

## 5. Contexto del proyecto

**Objetivo principal:** Crear un programa que identifique qué **tarea del catálogo de tareas** corresponde a cada registro del JSON, extraído del sistema de gestión documentaria **Qamaqi - Gobierno Regional Tacna**.

**Próximo paso:** Definir el catálogo de tareas y diseñar el clasificador.

---

## 6. Commits realizados

| Commit | Descripción |
|---|---|
| `6a49c57` | Initial commit: add .gitignore |
| `47145be` | Add CLAUDE.md |
| `ed8ea48` | add download script and projects list |
