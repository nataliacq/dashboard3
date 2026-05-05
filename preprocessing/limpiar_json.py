import json
import unicodedata


def limpiar(s):
    if not s:
        return s
    s = s.strip()
    s = s.replace('\n', ' ').replace('\r', ' ')
    s = unicodedata.normalize('NFD', s)
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
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


INPUT  = 'proyectos_data.json'
OUTPUT = 'proyectos_data_clean.json'

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
