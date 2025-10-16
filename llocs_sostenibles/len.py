import json 
with open('llocs_sostenibles.json', 'r', encoding='utf-8') as fitxer:
    dades = json.load(fitxer)
print(len(dades))
