import json
import re
import unicodedata
from pathlib import Path


# Caracteres tipográficos -> equivalente ASCII (no son marcas combinantes,
# por eso NFD no los toca y hay que reemplazarlos a mano).
_REEMPLAZOS = {
    '‘': "'", '’': "'",   # comillas simples curvas ' '
    '“': '"', '”': '"',   # comillas dobles curvas " "
    '–': '-', '—': '-',   # guiones largos - -
    '…': '...',                # puntos suspensivos
    '°': '', 'º': '', 'ª': '',  # grado y ordinales
    ' ': ' ',                  # espacio no separable
}


def limpiar(s):
    if not s:
        return s
    # saltos de linea, retornos y tabulaciones -> espacio
    s = re.sub(r'[\r\n\t]+', ' ', s)
    # reemplaza caracteres tipograficos por su equivalente ASCII
    for orig, repl in _REEMPLAZOS.items():
        s = s.replace(orig, repl)
    # quita tildes/diacriticos (NFD + elimina marcas combinantes)
    s = unicodedata.normalize('NFD', s)
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    # descarta cualquier caracter no-ASCII restante
    s = s.encode('ascii', 'ignore').decode('ascii')
    # colapsa espacios multiples y recorta extremos
    s = re.sub(r' +', ' ', s).strip()
    return s


def limpiar_transaccion(t):
    t['origen']['oficina'] = limpiar(t['origen'].get('oficina'))
    t['destino']['oficina'] = limpiar(t['destino'].get('oficina'))
    t['origen']['nombre']   = limpiar(t['origen'].get('nombre'))
    t['destino']['nombre']  = limpiar(t['destino'].get('nombre'))
    t['proveidos'] = [limpiar(p) for p in t.get('proveidos', [])]


def limpiar_doc(doc):
    doc['documento_desc'] = limpiar(doc.get('documento_desc'))
    for t in doc.get('transacciones', []):
        limpiar_transaccion(t)


ROOT   = Path(__file__).resolve().parent.parent
INPUT  = ROOT / 'proyectos_data.json'
OUTPUT = ROOT / 'data' / 'proyectos_data_clean.json'

with open(INPUT, encoding='utf-8') as f:
    data = json.load(f)

for cui, docs in data.items():
    for doc in docs:
        limpiar_doc(doc['documento_principal'])
        for hijo in doc.get('documentos_hijos', []):
            limpiar_doc(hijo)

with open(OUTPUT, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'Guardado en {OUTPUT}')
