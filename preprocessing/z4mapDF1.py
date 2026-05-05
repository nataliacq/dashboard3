from __future__ import annotations

import json
from itertools import count
from pathlib import Path

import pandas as pd

_DATA_PATH = Path(__file__).parent.parent / "data" / "dataClean4.json"
_OUTPUT_DIR = Path(__file__).parent.parent / "data"
_DATE_FMT = "%d/%m/%Y %H:%M:%S"


def _parse_fecha(s: str | None) -> pd.Timestamp | None:
    if not s:
        return None
    try:
        return pd.to_datetime(s, format=_DATE_FMT)
    except Exception:
        return None


def _next_csv_path(stem: str = "dataframe") -> Path:
    p = _OUTPUT_DIR / f"{stem}.csv"
    if not p.exists():
        return p
    i = 2
    while True:
        p = _OUTPUT_DIR / f"{stem}{i}.csv"
        if not p.exists():
            return p
        i += 1


def generar_df1(data: dict | None = None) -> pd.DataFrame:
    if data is None:
        with open(_DATA_PATH, encoding="utf-8") as f:
            data = json.load(f)

    mov_counter = count(1)
    rows = []

    for cui, entries in data.items():
        for obj in entries:
            dp = obj["documento_principal"]
            hijos = obj.get("documentos_hijos", [])

            adj_cuds = ";".join(h["documento_cud"] for h in hijos)
            adj_descs = ";".join(h["documento_desc"] for h in hijos)
            adj_list = [h["documento_desc"] for h in hijos]

            docs = [(dp, adj_list, adj_cuds, adj_descs)] + [
                (hijo, [], "", "") for hijo in hijos
            ]

            for doc, doc_adj_list, doc_adj_cuds, doc_adj_descs in docs:
                transacciones = doc.get("transacciones", [])
                cud = doc["documento_cud"]
                desc = doc["documento_desc"]

                derivados = [t for t in transacciones if t["tipo_movimiento"] == "DERIVADO"]
                recibidos = [t for t in transacciones if t["tipo_movimiento"] == "RECIBIDO"]

                groups: dict[tuple, list] = {}
                for d in derivados:
                    key = (
                        d["fecha_mov"],
                        (d["origen"]["oficina"] or "").strip(),
                        d["origen"]["nombre"] or "",
                    )
                    groups.setdefault(key, []).append(d)

                for (fecha_deriv, orig_of, orig_nm), group in groups.items():
                    mov_code = next(mov_counter)

                    for deriv in group:
                        dest_of = (deriv["destino"]["oficina"] or "").strip()
                        dest_nm = deriv["destino"]["nombre"] or ""

                        pair = next(
                            (
                                r for r in recibidos
                                if (r["origen"]["oficina"] or "").strip() == orig_of
                                and (r["origen"]["nombre"] or "") == orig_nm
                                and (r["destino"]["oficina"] or "").strip() == dest_of
                                and (r["destino"]["nombre"] or "") == dest_nm
                            ),
                            None,
                        )

                        rows.append({
                            "CUI": cui,
                            "codigo_mov": mov_code,
                            "documento_desc": desc,
                            "fecha_derivado": _parse_fecha(fecha_deriv),
                            "fecha_recibido": _parse_fecha(pair["fecha_mov"]) if pair else None,
                            "documento_cud": cud,
                            "origen_oficina": orig_of,
                            "origen_nombre": orig_nm,
                            "destino_oficina": dest_of,
                            "destino_nombre": dest_nm,
                            "adjunto": doc_adj_list,
                            "adjCUD": doc_adj_cuds,
                            "adjDocDesc": doc_adj_descs,
                            "transac_id_recepcion": pair["transac_id"] if pair else None,
                        })

    df = pd.DataFrame(rows)

    csv_path = _next_csv_path()
    df.to_csv(csv_path, index=False, encoding="utf-8")

    return df
