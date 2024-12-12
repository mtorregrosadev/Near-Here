import json 
import math 
class LLocs_sostenibles:
    def __init__(self,latitud, longitud, radius):
        self.latitud = latitud 
        self.longitud = longitud
        self.radius = radius
    def distancia(self, dada): #La fórmula de Haversine
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
        if d > self.radius:
            return False
        else:
            print(d)
            return True
    def cerca_de_llocs(self):
        with open('llocs_sostenibles.json', 'r', encoding='utf-8') as fitxer:
            dades = json.load(fitxer)
        for i in range(len(dades)):
            distancia_t = self.distancia(dades[i])
            if distancia_t:
                print(f"Si! {dades[i]['name']}")

        

hola = LLocs_sostenibles(41.390097029404764,2.174703404632969,1000) 
prova = hola.cerca_de_llocs()
    