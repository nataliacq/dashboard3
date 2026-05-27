import requests
import json
import sys
import time
from pathlib import Path

API_BASE = "http://10.128.145.23/api-cui/api.php"
SCRIPT_DIR = Path(__file__).resolve().parent
LISTA_FILE = SCRIPT_DIR.parent / "data" / "proyectosList"
JSON_BASE = Path(r"C:\Users\HP\Documents\OneDrive\OPMI_2026\a oxi dash\v1 TRAZABILIDAD OXI DASHBOARD\json")

def siguiente_version():
    nums = [
        int(p.name[1:])
        for p in JSON_BASE.iterdir()
        if p.is_dir() and p.name.startswith("v") and p.name[1:].isdigit()
    ]
    return max(nums) + 1 if nums else 1

def cargar_codigos():
    with open(LISTA_FILE, encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def descargar_proyecto(cui):
    try:
        resp = requests.get(API_BASE, params={"cui": cui}, timeout=15)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"No se pudo consultar la API para CUI {cui}: {e}") from e
    except ValueError as e:
        raise RuntimeError(f"La API devolvió una respuesta no JSON para CUI {cui}") from e

def main():
    global LISTA_FILE
    if len(sys.argv) > 1:
        LISTA_FILE = Path(sys.argv[1])
    codigos = cargar_codigos()
    version = siguiente_version()
    carpeta = JSON_BASE / f"v{version}"
    carpeta.mkdir(parents=True, exist_ok=False)
    output = carpeta / "proyectos_data.json"

    print(f"Descargando {len(codigos)} proyectos -> {carpeta}")

    resultados = {}
    errores = []

    for i, cui in enumerate(codigos, 1):
        try:
            data = descargar_proyecto(cui)
            resultados[cui] = data
            print(f"[{i}/{len(codigos)}] {cui} OK")
        except Exception as e:
            errores.append(cui)
            print(f"[{i}/{len(codigos)}] {cui} ERROR: {e}")
        time.sleep(0.2)

    output.write_text(json.dumps(resultados, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nGuardado en {output}")
    print(f"Exitosos: {len(resultados)} | Errores: {len(errores)}")
    if errores:
        print(f"CUIs con error: {errores}")

if __name__ == "__main__":
    main()
