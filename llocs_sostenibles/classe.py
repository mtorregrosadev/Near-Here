import json 
import math 
class LLocs_sostenibles:
    def __init__(self,latitud, longitud, radius, limit, loc_visited, categories_sel):
        self.latitud = latitud 
        self.longitud = longitud
        self.radius = radius
        self.limit = limit
        self.loc_visited = loc_visited 
        self.categories_s = categories_sel
    def distancia(self, dada, bool): #La fórmula de Haversine
        latitude_inicial = math.radians(self.latitud)
        longitude_inicial = math.radians(self.longitud)
        latitude_final = math.radians(dada['latitude'])
        longitude_final = math.radians(dada['longitude'])
        # Ara després de passar a radians el que fem és fer la diferencia entre latituds i longituds.
        dif_1 = latitude_final  - latitude_inicial
        dif_2 = longitude_final  - longitude_inicial
        #Apliquem la formula ara 
        a = math.sin(dif_1/2)**2 + math.cos(latitude_inicial) * math.cos(latitude_final) * math.sin(dif_2/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        R = 6371000 # I multipliquem pel radi de la terra
        d = R * c
        if not bool:
            if d > self.radius:
                return False
            else:
                print(d)
                return True
        if bool:
            return d
    def dades(self):
        self.dades = []
        with open('llocs_sostenibles.json', 'r', encoding='utf-8') as fitxer:
            dades = json.load(fitxer)
        for i in range(len(dades)):
            distancia_t = self.distancia(dades[i], False)
            if distancia_t:
                self.dades.append(dades[i])
        # Sort self.dades based on distance
        self.dades.sort(key=lambda x: self.distancia(x, True))
        if len(self.dades) > self.limit:
            self.dades = self.dades[:self.limit]
        if self.categories_s:
            for i in range(len(self.dades) - 1, -1, -1):
                # Convertir les categories a enters
                categories_numeros = [int(num) for num in self.dades[i]['categories']]
                # Comprovar si hi ha alguna coincidència
                hi_es = any(num in self.categories_s for num in categories_numeros)
                print(hi_es, self.dades[i]['name'])
                if not hi_es:
                    del self.dades[i]
        self.data = []
        for i in range(len(self.dades)):
            lloc = self.dades[i]
            data_lloc = {
                "fsq_id": lloc.get('id', None),
                "alias": lloc.get('alias', None),
                "name": lloc.get('name', None),
                "photos": lloc.get('photos', None),
                "url": lloc.get('details', {}).get('website', None),
                "categories": lloc.get('categories', []),
                "coordinates": lloc.get('coordinates', {}),
                "location": {
                    "address": lloc.get("details", {}).get("address", None),
                    "address_extended": lloc.get("details", {}).get("adress", None),
                    "locality": lloc.get("details", {}).get("city", None),
                    "region": lloc.get("details", {}).get("city", None),
                    "postcode": lloc.get("details", {}).get("postal_code", None),
                    "country": lloc.get("details", {}).get("city", None)
                },
                "geocodes": {
                    "main": {
                        "latitude": lloc.get('latitude', None),
                        "longitude": lloc.get('longitude', None),
                    }
                },
            }
            self.data.append(data_lloc)
        return self.data 
    
    def photos(self):
        fotos = []
        for i in range(len(self.dades)):
            if 'photos' in self.dades[i]:
                fotos.append(self.dades[i]['photos'])
            else:
                fotos.append([])
        return fotos
        

lloc_sostenibles = LLocs_sostenibles(42.12510989376849,2.8682060185206506,1000,50,[],[14]) 
Dades = lloc_sostenibles.dades()
fotos = lloc_sostenibles.photos()
    