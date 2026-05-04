import math 
import logging
import random 
import json
import os
import requests
import httpx

logger = logging.getLogger('NearHere')

class LLocs_sostenibles:
    def __init__(self,latitud, longitud, radius, limit, loc_visited, categories_sel):
        self.latitud = latitud 
        self.longitud = longitud
        self.radius = radius
        self.limit = limit
        self.loc_visited = loc_visited 
        self.categories_s = categories_sel
        logger.info(f"LLocs_sostenibles inicialitzat - Lat: {latitud}, Long: {longitud}, Radius: {radius}m, Limit: {limit}, Categories: {categories_sel}")
    
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
                logger.debug(f"Lloc dins el radi: {dada.get('name', 'Desconegut')} - Distancia: {d:.2f}m")
                return True
        if bool:
            return d
    
    def dades(self):
        logger.info("Iniciant cerca de llocs sostenibles")
        self.dades = []
        try:
            with open('llocs_sostenibles.json', 'r', encoding='utf-8') as fitxer:
                dades = json.load(fitxer)
            logger.info(f"Fitxer JSON carregat correctament - Total llocs: {len(dades)}")
        except FileNotFoundError:
            logger.error("ERROR: Fitxer llocs_sostenibles.json no trobat")
            return "error 400 de l'API sostenible", self.loc_visited
        except json.JSONDecodeError as e:
            logger.error(f"ERROR: Error llegint JSON - {str(e)}")
            return "error 400 de l'API sostenible", self.loc_visited
        
        logger.info(f"Buscant llocs dins un radi de {self.radius}m des de ({self.latitud}, {self.longitud})")
        for i in range(len(dades)):
            distancia_t = self.distancia(dades[i], False)
            if distancia_t:
                self.dades.append(dades[i])
        logger.info(f"Llocs trobats dins el radi: {len(self.dades)}")
        
        # Sort self.dades based on distance
        self.dades.sort(key=lambda x: self.distancia(x, True))
        if len(self.dades) > self.limit:
            logger.debug(f"Limitant resultats de {len(self.dades)} a {self.limit}")
            self.dades = self.dades[:self.limit]
        
        if self.categories_s: # Si es [] no fa res, en canvi si conté algo serà True
            logger.info(f"Filtrant per categories: {self.categories_s}")
            llocs_abans_filtrar = len(self.dades)
            for i in range(len(self.dades) - 1, -1, -1):
                # Convertir les categories a enters
                categories_numeros = [int(num) for num in self.dades[i]['categories']]
                # Comprovar si hi ha alguna coincidència
                hi_es = any(num in self.categories_s for num in categories_numeros)
                logger.debug(f"Lloc '{self.dades[i]['name']}' - Categories: {categories_numeros} - Coincideix: {hi_es}")
                if not hi_es:
                    del self.dades[i]
            logger.info(f"Llocs despres de filtrar per categories: {len(self.dades)} (abans: {llocs_abans_filtrar})")
        
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
        
        logger.info(f"Total llocs processats i retornats: {len(self.data)}")
        if self.data == []:
            logger.warning("Cap lloc sostenible trobat amb els criteris actuals")
            return "error 400 de l'API sostenible", self.loc_visited
        else:
            logger.info(f"Retornant {len(self.data)} llocs sostenibles")
            return self.data, self.loc_visited
    
    def photos(self):
        fotos = []
        for i in range(len(self.dades)):
            if 'photos' in self.dades[i]:
                fotos.append(self.dades[i]['photos'])
            else:
                fotos.append([])
        return fotos
    
    def categories(self):
        categories = []
        for i in range(len(self.data)):
            categories.append([])
        return categories   

class Llocs:
    def __init__(self, latitud, longitud, radius, limit, loc_visited,categories_sel, sort_sel, preu, near): 
        #Definim totes les variables que hem donat a traves de la class
        self.latitud = latitud 
        self.longitud = longitud
        self.radius = radius
        self.limit = limit
        self.loc_visited = loc_visited
        self.categories_s = categories_sel
        self.sort = sort_sel
        self.preu = preu
        self.near = near
        logger.info(f"Llocs (Foursquare) inicialitzat - Lat: {latitud}, Long: {longitud}, Radius: {radius}m, Limit: {limit}, Sort: {sort_sel}, Preu: {preu}, Near: {near}")

    def _randomize_coordinates(self, lat, lon):
        # Afegeix un petit desplaçament a les coordenades perquè no sigui sempre igual
        increment = len(self.loc_visited) / 10000
        logger.debug(f"increment és: {increment}")
        if len(self.loc_visited) > 1 and len(self.loc_visited) < 100: 
            # Aquest el que fa es detectar la longitud de les places ja visitades i depenent d'aquesta fa més variació o menys
            randloc = (len(self.loc_visited) // 10) * increment
        elif len(self.loc_visited) >= 100: 
            # Aquí fem que hi hagi més variació al segon que al primer
            randloc = (len(self.loc_visited) // 5) * increment
            # La variació màxima seria de 1,5Km
        else:
            return lat,lon 
        new_lat = lat + random.uniform(-randloc, randloc)
        new_lon = lon + random.uniform(-randloc, randloc)
        return new_lat, new_lon #Retorna les localitzacions randomitzades
    def dades(self): #Aqui agafem totes les dades 
        logger.info("Iniciant cerca de llocs amb Foursquare API")
        data=[]
        tcategories = ""
        if len(self.categories_s) > 0:
            for i in range(len(self.categories_s)): #Això el que fa es comprovar si tens categories per cercar i juntar-les amb una coma.
                tcategories = ",".join(str(a) for a in self.categories_s)
            logger.debug(f"Categories formatades per API: {tcategories}")

        #print(tcategories)
        randomized_lat, randomized_lon = self._randomize_coordinates(self.latitud, self.longitud) if not self.near or self.near == "" else (self.latitud, self.longitud)
        #Rep les coordenades randomitzades 
        logger.debug(f"Coordenades utilitzades: ({randomized_lat}, {randomized_lon})")
        
        url = "https://places-api.foursquare.com/places/search"
        headers = {
            "accept": "application/json",
            "X-Places-Api-Version": "2025-06-17",
            "Authorization": os.getenv("FOURSQUARE_API_KEY")
        }
        params = {
            "ll": f"{randomized_lat},{randomized_lon}",
            "radius": self.radius,
            "limit": self.limit, 
            # Tots aquests parametres serán obligatoris
            "fields": "fsq_id,name,geocodes,location,categories,related_places,timezone,closed_bucket,social_media,rating,price,photos,menu,distance,chains", 
            "sort": self.sort,
        }

        if self.preu != 0:
            params["max_price"] = self.preu
            logger.debug(f"Filtre de preu aplicat: max_price={self.preu}")
        if tcategories != "":
            params["categories"] = tcategories
        if self.near is not None and self.near != "":
            params["near"] = self.near
            del params["ll"]
            del params["radius"]
            logger.info(f"Cerca amb lloc especific: {self.near}")
            logger.debug(f"Parametres API: {params}")

        logger.info(f"Enviant peticio a Foursquare API - Radius: {self.radius}m, Limit: {self.limit}")
        try:
            locations = requests.get(url, headers=headers, params=params, timeout=15)
            
            #Detecta si l'API l'ha contestat 200 == Bé i després detecta que no sigui ja a la llista
            if locations.status_code == 200:
                logger.info(f"Resposta Foursquare API: Status 200 OK")
                locations = locations.json()
                if 'results' in locations:
                    total_results = len(locations['results'])
                    logger.info(f"Resultats rebuts: {total_results}")
                    for loc in locations['results']:
                        if loc['fsq_id'] not in [visited['fsq_id'] for visited in self.loc_visited]:
                            data.append(loc)
                            self.loc_visited.append(loc)
                    logger.info(f"Llocs nous (no visitats): {len(data)}")
                else:
                    logger.error("ERROR: Camp 'results' no trobat a la resposta de l'API")
            elif locations.status_code == 400:
                logger.error(f"ERROR 400 Foursquare API - Resposta: {locations.text}")
                return "error 400", self.loc_visited
            else:
                logger.error(f"ERROR {locations.status_code} Foursquare API - Resposta: {locations.text}")
                return "error 400", self.loc_visited
        except requests.exceptions.RequestException as e:
            logger.error(f"ERROR de connexió a Foursquare API: {str(e)}")
            return "error 500", self.loc_visited
        except Exception as e:
            logger.error(f"ERROR desconegut a Foursquare API: {str(e)}")
            return "error 500", self.loc_visited

        self.data = data
        logger.info(f"Retornant {len(data)} llocs de Foursquare")
        return data, self.loc_visited

    
    def photos(self):
        photos = []
        for d in range(len(self.data)):
            llocs_photos = []
            if 'photos' in self.data[d]:
                for i in range(len(self.data[d]['photos'])):
                    photo = self.data[d]['photos'][i]['prefix'] + str(self.data[d]['photos'][i]['width']) + "x" + str(self.data[d]['photos'][i]['height']) + self.data[d]['photos'][i]['suffix']
                    llocs_photos.append(photo)
                photos.append(llocs_photos)
            else:
                photos.append([])
        return photos
    def categories(self): #Recopila les categories per cada lloc 
        fsq_categories = []
        for i in range(len(self.data)):
            categories = []
            data = self.data[i]
            for category in data['categories']:
                icon_prefix = category['icon']['prefix'] + "120" + category['icon']['suffix']
                categories.append(icon_prefix)
            fsq_categories.append(categories)
        return fsq_categories

class Llocs_info:
    def __init__(self, fsq_id):
        self.fsq_id = fsq_id 
    async def search_data(self):

        url = f"https://api.foursquare.com/v3/places/{self.fsq_id}"

        headers = {
            "accept": "application/json",
            "Authorization": os.getenv("FOURSQUARE_API_KEY")
        }
        params = {
            "fields": "description,tel,email,website,social_media,hours,hours_popular,rating,stats,popularity,price,menu,photos,tastes,features,venue_reality_bucket,related_places,timezone,distance"
        }
        async with httpx.AsyncClient() as client:  # Crea una sessió asíncrona amb httpx
            response = await client.get(url, headers=headers, params=params)  # Utilitza client.get() per fer la petició
            if response.status_code == 200:  # Comprova l'estat de la resposta
                api_response = response.json()  # Espera la resposta JSON
                return api_response
            
class Llocs_Yelp_info:
    def __init__(self, fsq_id):
        self.fsq_id = fsq_id
    async def search_data(self):
        url = f"https://api.yelp.com/v3/businesses/{self.fsq_id}"

        headers = {
            "accept": "application/json",
            "Authorization": os.getenv("YELP_API_KEY")
        }
        async with httpx.AsyncClient() as client:  # Crea una sessió asíncrona amb httpx
            response = await client.get(url, headers=headers)  # Utilitza client.get() per fer la petició
            if response.status_code == 200:  # Comprova l'estat de la resposta
                api_response = response.json()  # Espera la resposta JSON
                return api_response
            else:
                Page.go("/error")
                       
class Llocs_yelp:
    def __init__(self, latitud, longitud, radius, limit, loc_visited,categories_sel, sort_sel, preu, near): #Definim totes les variables que hem donat a traves de la class
        self.latitud = latitud 
        self.longitud = longitud
        self.radius = radius
        self.limit = limit
        self.loc_visited = loc_visited
        self.categories_s = categories_sel
        self.sort = sort_sel
        self.preu = preu
        self.near = near
        logger.info(f"Llocs_yelp inicialitzat - Lat: {latitud}, Long: {longitud}, Radius: {radius}m, Limit: {limit}, Sort: {sort_sel}, Preu: {preu}, Near: {near}")

    def _randomize_coordinates(self, lat, lon):
        # Afegeix un petit desplaçament a les coordenades perquè no sigui sempre igual
        increment = len(self.loc_visited) / 10000
        logger.debug(f"increment és: {increment}")
        if len(self.loc_visited) > 1 and len(self.loc_visited) < 100: #Aquest el que fa es detectar la longitud de les places ja visitades i depenent d'aquesta fa més variació o menys
            randloc = (len(self.loc_visited) // 10) * increment
        elif len(self.loc_visited) >= 100: 
            self.limit += 2
            randloc = (len(self.loc_visited) // 10) * increment
        else:
            return lat,lon 
        new_lat = lat + random.uniform(-randloc, randloc)
        new_lon = lon + random.uniform(-randloc, randloc)
        return new_lat, new_lon #Retorna les localitzacions randomitzades
    
    def dades(self): #Aqui agafem totes les dades 
        logger.info("Iniciant cerca de llocs amb Yelp API")
        data=[]
        #print(tcategories)
        tcategories = ""
        categories_yelp = {
            # Tags_amunt
            13065: "restaurants",
            16020: "publicplazas",
            16026: "castles",
            16031: "museums",
            16051: "culturalcenter",
            16032: "parks",
            13037: "coffee",
            10000: "amusementparks",
            12080: "arcades",
            17018: "musicvenues",
            17000: "shopping",
            
            # Tourism-related categories
            10001: "amusementparks",
            10003: "tours",
            10004: "museums",
            10009: "sailing",
            10027: "museums",
            16011: "historicalsites",
            16034: "nationalparks",
            16024: "gardens",
            16014: "observatories",
            16007: "beaches",

            # General Categories
            13000: "food",
            16000: "outdooractivities",
            10000: "artsentertainment",
            19000: "travelservices",
            
            # Menjar (Food) Specific Categories
            13002: "bakeries",
            13003: "bars",
            13041: "creperies",
            13390: "glutenfree",

            # Outdoor Categories
            16003: "beaches",
            16026: "landmarks",

            # Entertainment Specific
            10021: "karaoke",
            10015: "escapegames",
            10006: "bowling",
            10024: "movietheaters",

            # Travel Categories
            19002: "bikerentals",
            19003: "boatrentals",
            19009: "hotels",
            19020: "ecoparking",
            19024: "reststops",
            19055: "sustainabletourism",

            # Shops
            17039: "ecofashion",
            17114: "shoppingcenters",
            17018: "bookstores",
            17029: "convenience",
            17138: "vintage",
            17056: "florists",
            17135: "toys",
            17057: "organic"
        }
        logger.debug(f"Categories Yelp abans de processar: {tcategories}")
        if len(self.categories_s) > 0:
            logger.debug(f"Processant {len(self.categories_s)} categories seleccionades")
            for i in range(len(self.categories_s)):
                category = categories_yelp.get(self.categories_s[i],[])
                category_af = f"{category},"
                tcategories = tcategories + category_af
            logger.debug(f"Categories Yelp formatades: {tcategories}")



        randomized_lat, randomized_lon = self._randomize_coordinates(self.latitud, self.longitud) if self.near is None or self.near == "" else (self.latitud, self.longitud) #Rep les coordenades randomitzades 
        logger.debug(f"Coordenades utilitzades: ({randomized_lat}, {randomized_lon})")
        
        url = "https://api.yelp.com/v3/businesses/search"
        headers = {
            "accept": "application/json",
            "Authorization": os.getenv("YELP_API_KEY")
        }
        if self.sort == "RATING":
            self.sort.lower()
        elif self.sort == "RELEVANCE":
            self.sort = "best_match"
        elif self.sort =="DISTANCE":
            self.sort.lower()
        elif self.sort == "POPULARITY":
            self.sort = "review_count"
        logger.debug(f"Parametres cerca: Radius={self.radius}, Limit={self.limit}, Sort={self.sort}")
        params = {
            "latitude": f"{randomized_lat}",
            "longitude": f"{randomized_lon}",
            "radius": self.radius,
            "limit": self.limit, # Tots aquests parametres serán obligatoris
            "sort": self.sort,
            "categories": "farmersmarket,organicstores,ethicalgrocery,csa,bikeparking,parks,beaches,gardens,streetvendors,hiking,publicplazas,playgrounds,wineries,salumerie,seafoodmarkets,culturalcenter,visitorcenters,recyclingcenter"
        }

        if self.preu != 0: # Comprova si és 0 per tal de no aplicar filtre ja que es del 1 al 4
            params["price"] = self.preu
            logger.debug(f"Filtre de preu aplicat: {self.preu}")
        if tcategories != "":
            logger.debug(f"Afegint categories personalitzades: {tcategories}")
            params['categories'] = tcategories + "farmersmarket,organicstores,ethicalgrocery,csa,bikeparking,parks,beaches,gardens,streetvendors,hiking,publicplazas,playgrounds,wineries,salumerie,seafoodmarkets,culturalcenter,visitorcenters,recyclingcenter"
        if self.near is not None and self.near != "": #Elimina i canvia el lloc en el cas que hi hagi un lloc indicat
            params["location"] = self.near
            del params["latitude"]
            del params["longitude"]
            del params["radius"]
            logger.info(f"Cerca amb lloc especific: {self.near}")
            logger.debug(f"Parametres API: {params}")

        logger.info(f"Enviant peticio a Yelp API - Radius: {self.radius}m, Limit: {self.limit}")
        
        try:
            locations = requests.get(url, headers=headers, params=params, timeout=15)
            
            #Detecta si l'API l'ha contestat 200 == Bé i després detecta que no sigui ja a la llista
            if locations.status_code == 200:
                logger.info(f"Resposta Yelp API: Status 200 OK")
                locations = locations.json().get('businesses', [])
                logger.info(f"Resultats rebuts de Yelp: {len(locations)}")
                for i in range(len(locations)):
                    lloc = locations[i]
                    if 'price' in lloc:
                        lloc['price'] = len(lloc['price'])
                    data_lloc = {
                        "fsq_id": lloc.get('id', None),
                        "alias": lloc.get('alias', None),
                        "name": lloc.get('name', None),
                        "photos": lloc.get('image_url', None),
                        "is_closed": lloc.get('is_closed', None),
                        "url": lloc.get('url', None),
                        "review_count": lloc.get('review_count', None),
                        "categories": lloc.get('categories', []),
                        "closed_bucket": "Closed" if lloc.get("is_closed") else "Open",
                        "rating": lloc.get('rating', None),
                        "coordinates": lloc.get('coordinates', {}),
                        "transactions": lloc.get('transactions', []),
                        "price": lloc.get('price', None),
                        "location": {
                            "address": lloc.get("location", {}).get("address1", None),
                            "address_extended": lloc.get("location", {}).get("address2", None),
                            "locality": lloc.get("location", {}).get("city", None),
                            "region": lloc.get("location", {}).get("state", None),
                            "postcode": lloc.get("location", {}).get("zip_code", None),
                            "country": lloc.get("location", {}).get("country", None)
                        },
                        "geocodes": {
                            "main": {
                                "latitude": lloc.get("coordinates", {}).get("latitude", None),
                                "longitude": lloc.get("coordinates", {}).get("longitude", None)
                            }
                        },
                        "phone": lloc.get('phone', None),
                        "display_phone": lloc.get('display_phone', None),
                        "distance": lloc.get('distance', None),
                        "business_hours": lloc.get('hours', []),
                        "attributes": lloc.get('attributes', {})
                    }
                    data.append(data_lloc)
                    logger.debug(f"Lloc afegit: {data_lloc['name']}")
                #! He de posar sistema per treure els llocs visitats!!
            else:
                if locations.status_code == 400:
                    logger.error(f"ERROR 400 Yelp API - Resposta: {locations.text}")
                else:
                    logger.error(f"ERROR {locations.status_code} Yelp API - Resposta: {locations.text}")
                return "error 400", self.loc_visited
        except requests.exceptions.RequestException as e:
            logger.error(f"ERROR de connexió a Yelp API: {str(e)}")
            return "error 500", self.loc_visited
        except Exception as e:
            logger.error(f"ERROR desconegut a Yelp API: {str(e)}")
            return "error 500", self.loc_visited

        self.data = data
        
        if self.data == []:
            return "error 400", self.loc_visited
        else:
            return data, self.loc_visited
    
    def photos(self):
        fotos = []
        
        for i in range(len(self.data)):
            fotos_llocs = []
            logger.debug(self.data[i]['photos'])
            if 'photos' in self.data[i]:
                fotos_llocs.append(self.data[i]['photos'])
                fotos.append(fotos_llocs)
            else:
                fotos.append([])
        logger.debug(fotos)
        return fotos
    def categories(self):
        #! Per fer 
        categories = []
        for i in range(len(self.data)):
            categories.append([])
        return categories   
