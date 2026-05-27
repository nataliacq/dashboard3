from __future__ import annotations

import json
from pathlib import Path


# ── I/O ──────────────────────────────────────────────────────────────────────

def cargar(path: str | Path) -> dict:
    """Carga un JSON desde disco y devuelve el dict."""
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def guardar(data: dict, path: str | Path) -> None:
    """Guarda el dict como JSON (UTF-8, indent=2, ensure_ascii=False)."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ── Filtros ───────────────────────────────────────────────────────────────────

def filtrar_sin_transacciones(data: dict) -> tuple[dict, dict]:
    """
    Elimina los objetos cuyo documento_principal.transacciones esté vacío o ausente.
    Si un CUI queda sin entradas, se elimina también la clave CUI.
    Devuelve (data_filtrada, stats) con keys "eliminados" y "conservados".
    """
    resultado = {}
    eliminados = 0
    conservados = 0
    for cui, entries in data.items():
        filtrados = [
            obj for obj in entries
            if obj.get("documento_principal", {}).get("transacciones")
        ]
        eliminados += len(entries) - len(filtrados)
        conservados += len(filtrados)
        if filtrados:
            resultado[cui] = filtrados
    return resultado, {"eliminados": eliminados, "conservados": conservados}


def marcar_auto_derivaciones(data: dict) -> tuple[dict, dict]:
    """
    Marca tipo_movimiento = "EXTERNO" cuando origen.nombre == destino.nombre
    (la misma persona se deriva a sí misma).
    Devuelve (data, stats) con key "marcados".
    """
    marcados = 0
    for entries in data.values():
        for obj in entries:
            for t in obj.get("documento_principal", {}).get("transacciones", []):
                origen = t.get("origen", {})
                destino = t.get("destino", {})
                if origen.get("nombre") and origen["nombre"] == destino.get("nombre"):
                    t["tipo_movimiento"] = "EXTERNO"
                    marcados += 1
    return data, {"marcados": marcados}


# ── Pipeline helper ───────────────────────────────────────────────────────────

def aplicar_filtros(data: dict, *filtros) -> dict:
    """
    Aplica una secuencia de funciones filtro a data.
    Cada filtro debe tener firma: (dict) -> tuple[dict, dict].
    Imprime el nombre y las stats de cada paso.
    """
    for fn in filtros:
        data, stats = fn(data)
        print(f"{fn.__name__}: {stats}")
    return data
