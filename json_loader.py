from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

DEFAULT_PATH = Path(__file__).parent / "proyectos_data_clean.json"

_DATE_FMT = "%d/%m/%Y %H:%M:%S"


def cargar_datos(path: str | Path = DEFAULT_PATH) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _iter_documentos(data: dict):
    for cui, entries in data.items():
        for obj in entries:
            yield cui, obj


def buscar_por_documento_id(data: dict, doc_id: int) -> dict | None:
    for _, obj in _iter_documentos(data):
        if obj["documento_principal"]["documento_id"] == doc_id:
            return obj
    return None


def buscar_por_cud(data: dict, cud: str) -> dict | None:
    for _, obj in _iter_documentos(data):
        if obj["documento_principal"]["documento_cud"] == cud:
            return obj
    return None


def _parse_fecha(s: str | None) -> pd.Timestamp | None:
    if not s:
        return None
    try:
        return pd.to_datetime(s, format=_DATE_FMT)
    except Exception:
        return None


def df_documentos(data: dict) -> pd.DataFrame:
    rows = []
    for cui, obj in _iter_documentos(data):
        dp = obj["documento_principal"]
        rows.append({
            "cui": cui,
            "documento_id": dp["documento_id"],
            "documento_cud": dp["documento_cud"],
            "documento_desc": dp["documento_desc"],
            "fecha_registro": _parse_fecha(dp.get("fecha_registro")),
            "num_transacciones": len(dp.get("transacciones", [])),
            "num_hijos": len(obj.get("documentos_hijos", [])),
        })
    return pd.DataFrame(rows)


def df_transacciones(data: dict) -> pd.DataFrame:
    rows = []
    for cui, obj in _iter_documentos(data):
        dp = obj["documento_principal"]
        for t in dp.get("transacciones", []):
            rows.append({
                "cui": cui,
                "documento_id": dp["documento_id"],
                "documento_cud": dp["documento_cud"],
                "transac_id": t["transac_id"],
                "tipo_movimiento": t["tipo_movimiento"],
                "fecha_mov": _parse_fecha(t.get("fecha_mov")),
                "origen_nombre": t["origen"]["nombre"],
                "origen_oficina": t["origen"]["oficina"],
                "destino_nombre": t["destino"]["nombre"],
                "destino_oficina": t["destino"]["oficina"],
                "proveidos": "; ".join(t.get("proveidos", [])),
            })
    return pd.DataFrame(rows)


def df_hijos(data: dict) -> pd.DataFrame:
    rows = []
    for cui, obj in _iter_documentos(data):
        dp = obj["documento_principal"]
        for hijo in obj.get("documentos_hijos", []):
            rows.append({
                "cui": cui,
                "parent_documento_id": dp["documento_id"],
                "parent_documento_cud": dp["documento_cud"],
                "documento_id": hijo["documento_id"],
                "documento_cud": hijo["documento_cud"],
                "documento_desc": hijo["documento_desc"],
                "fecha_registro": _parse_fecha(hijo.get("fecha_registro")),
                "num_transacciones": len(hijo.get("transacciones", [])),
            })
    return pd.DataFrame(rows)
