import flet 
from flet import Page,Dropdown,dropdown,TextButton,Divider,View,border,Slider,Checkbox,RoundedRectangleBorder,TileAffinity,ExpansionTile,Geolocator,AnimatedSwitcherTransition,AppBar,Card,GridView,TextThemeStyle,ListTile, MainAxisAlignment,AnimatedSwitcher,Stack,Column,TextSpan,TextStyle,Paint,AlertDialog,IconButton, StrokeJoin,PaintingStyle,ShadowBlurStyle, BoxShadow, Image, ListTile,GestureDetector, FontWeight,ElevatedButton, SafeArea,Theme, animation, Container, transform, Icon, icons, colors, alignment, icons, Row, Text, ResponsiveRow, Chip, NavigationBarDestination, NavigationBar 
from math import pi
import asyncio
import json
import location
index_photo = 0
import requests
import random
import copy

images_request = []
index_photo_stack = -1
categories_sel_antic = []
canvi = False
cards = []
class Llocs:
    def __init__(self, latitud, longitud, radius, limit, loc_visited,categories_sel, sort_sel, preu): #Definim totes les variables que hem donat a traves de la class
        self.latitud = latitud 
        self.longitud = longitud
        self.radius = radius
        self.limit = limit
        self.loc_visited = loc_visited
        self.categories_s = categories_sel
        self.sort = sort_sel
        self.preu = preu

    def _randomize_coordinates(self, lat, lon):
        # Afegeix un petit desplaçament a les coordenades perquè no sigui sempre igual
        print(len(self.loc_visited))
        increment = len(self.loc_visited) / 10000
        print("increment és:", increment)
        if len(self.loc_visited) > 1 and len(self.loc_visited) < 100: #Aquest el que fa es detectar la longitud de les places ja visitades i depenent d'aquesta fa més variació o menys
            randloc = (len(self.loc_visited) // 10) * increment
        elif len(self.loc_visited) >= 100: 
            self.limit += 2
            randloc = (len(self.loc_visited) // 10) * increment
        else:
            return lat,lon #En cas de que sigui més de 120 (el qual es un canvi molt gran, 1,2 Km) ja retorna igual
        new_lat = lat + random.uniform(-randloc, randloc)
        new_lon = lon + random.uniform(-randloc, randloc)
        return new_lat, new_lon #Retorna les localitzacions randomitzades
    
    def dades(self): #Aqui agafem totes les dades 
        data=[]
        tcategories = ""
        if len(self.categories_s) > 0:
            for i in range(len(self.categories_s)): #Això el que fa es comprovar si tens categories per cercar i juntar-les amb una coma.
                tcategories = ",".join(str(a) for a in self.categories_s)

        #print(tcategories)
        randomized_lat, randomized_lon = self._randomize_coordinates(self.latitud, self.longitud) #Rep les coordenades randomitzades
        url = f"https://api.foursquare.com/v3/places/search"
        headers = {
            "accept": "application/json",
            "Authorization": "fsq3qcPa3WReZWK3a7h5flm4z4wKmecTbWUMl/Pot9hd1Bs="
        }
        if self.preu != 0:
            params = {
                "ll": f"{randomized_lat},{randomized_lon}",
                "radius": self.radius,
                "limit": self.limit, # Tots aquests parametres serán obligatoris
                "categories": tcategories if tcategories != "" else None, 
                "fields": "fsq_id,name,geocodes,location,categories,related_places,timezone,closed_bucket,social_media,rating,price,photos,menu,distance,chains", 
                "sort": self.sort,
                "max_price": self.preu
            }
        else:
            params = {
                "ll": f"{randomized_lat},{randomized_lon}",
                "radius": self.radius,
                "limit": self.limit, # Tots aquests parametres serán obligatoris
                "categories": tcategories if tcategories != "" else None, 
                "fields": "fsq_id,name,geocodes,location,categories,related_places,timezone,closed_bucket,social_media,rating,price,photos,menu,distance,chains", 
                "sort": self.sort,
            }

        locations = requests.get(url, headers=headers, params=params)
        
        #Detecta si l'API l'ha contestat 200 == Bé i després detecta que no sigui ja a la llista
        if locations.status_code == 200:
            locations = locations.json()
            if 'results' in locations:
                for loc in locations['results']:
                    if loc['fsq_id'] not in [visited['fsq_id'] for visited in self.loc_visited]:
                        data.append(loc)
                        self.loc_visited.append(loc)
            else:
                print("Error en la consulta de l'API")
       
        self.data = data
        return data, self.loc_visited

    
    def photos(self): #Cerca una foto per cada lloc
        if self.limit > 1:
            photos = []
            for d in range(len(self.data)):
                llocs_photos = []
                if 'photos' in self.data[d]:
                    for i in range(len(self.data[d]['photos'])):
                        photo = self.data[d]['photos'][i]['prefix'] + str(self.data[d]['photos'][i]['width']) + "x" + str(self.data[d]['photos'][i]['height']) + self.data[d]['photos'][i]['suffix']
                        llocs_photos.append(photo)
                    photos.append(llocs_photos)
                        # photo = "https://picsum.photos/300/400"
                        # photos.append(photo)
                else:
                    llocs_photos.append()
                    photos.append(llocs_photos)
            return photos
        elif self.limit == 1: 
            llocs_photos = []
            for d in range(len(self.data)):
                for i in range(len(self.data[d]['photos'])):
                    photo = self.data[d]['photos'][i]['prefix'] + str(self.data[d]['photos'][i]['width']) + "x" +  str(self.data[d]['photos'][i]['height'])  + self.data[d]['photos'][i]['suffix']
                    llocs_photos.append(photo)
            return llocs_photos
        else: 
            print("error")
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

async def main(page: Page):
    page.bgcolor = "#FFFCF1"
    page.title = "Near here..."
    page.window.width = 390
    page.window.height = 790
    page.horizontal_alignment = "center"
    page.theme_mode = "light"
    page.fonts = {
           "Proxima Nova": "fonts/ProximaNova-Regular.ttf",
           "Proxima Nova Bold": "fonts/ProximaNova-Bold.ttf",
           "Proxima Nova ExtraBold": "fonts/ProximaNova-ExtraBold.ttf",
           "Helvetica Neue": "fonts/HelveticaNeue-Regular.otf",
           "Stres": "fonts/Stres.otf",
           "WorkSans": "fonts/WorkSans-Black.ttf"
    }
    page.theme = Theme(font_family="Helvetica Neue")
    gl = Geolocator()
    page.add(gl)
    await gl.request_permission_async() 
    await location.handle_permission(gl,AlertDialog, page, Text,TextButton,MainAxisAlignment)
    page.update()
    page.session.set("categories_sel", [])
    page.session.set("categories_sel_antic",[])
    await page.client_storage.set_async("loc_visited", [])
    await page.client_storage.set_async("radius_sel", 1000)
    await page.client_storage.set_async("sort_sel", "RELEVANCE")
    await page.client_storage.set_async("preu", 0)

    
    def view_pop(event): #Per anar enrere 
        #print("view pop:", event.view) #Això només imprimeix en terminal, de normal no cal
        if page.route == '/categories' or page.route == '/info':
            page.views.pop()
            page.go('/')
        else: 
            page.views.pop()
            page.go("/configuracio")
       # top_view = page.views[-1]
        #  page.go(top_view.route)

    async def on_change_page(e):
        page.controls.clear() if page.route != '/info' else None
        page.add(gl)
        async def tornar(e):
            page.go("/")
        
        if page.route == '/':
            print("Seleccionat llocs!")
            selected_llocs.offset = transform.Offset(0,0)
            page.add(Tags_amunt_safe,stack_cards,botons)
            botons.opacity = 1
            Tags_amunt.opacity = 1
            stack_cards.opacity = 1
            cards[0].scale = 1
            cards[0].opacity = 1
   
        if page.route == '/favorits':
            print("Favorits seleccionat")
            images_saved.controls = []
            page.add(images_saved)
            if len(saved_cards) > 0:
                for i in range(len(saved_cards)):
                    images_saved.controls.append(
                        Container(content=Column(spacing=0.5,horizontal_alignment="center", controls=[Image(
                            src=f"https://picsum.photos/150/150?{i}",
                            border_radius=10), Text(f"{i}", text_align="center")
                    ])))
                    page.update()
            else:
                page.add(SafeArea(content=Text("No tens favorits!", text_align="center", height=page.height)))

        if page.route == '/configuracio':
            page.add(configuracio)
            print("Configuració seleccionada")

        if page.route == '/configuracio/historial': 
            def resize_image_url(url, width, height):
                # Part invariable de l'URL
                invariant_part = "https://fastly.4sqi.net/img/general/"
                
                # Busca la posició on comença la part variable (les dimensions i la resta de l'URL)
                start_index = len(invariant_part)
                
                # Obté la part variable de l'URL
                variable_part = url[start_index:]
                
                # Busca la primera part que coincideix amb el patró 'widthxheight'
                dimensions, remainder = variable_part.split('/', 1)
                
                # Substitueix les dimensions per les noves
                new_dimensions = f'{width}x{height}'
                
                # Construeix la nova URL
                new_url = invariant_part + new_dimensions + '/' + remainder
                
                return new_url
            
            loc_visited = await page.client_storage.get_async("loc_visited")  
            loc_visited_photos = await page.client_storage.get_async("loc_visited_photos")  
            page.add(configuracio)    
            images_saved.height = page.height
            images_saved.controls = []
            if len(loc_visited) > 0:
                page.views.append(View(controls=[AppBar(title=Text("Historial de Llocs"), adaptive=True,bgcolor="#AAD7D9"), images_saved],bgcolor = "#FFFCF1"))
                for i in range(len(loc_visited)):
                    if loc_visited_photos[i] != []:
                        url = loc_visited_photos[i][0]
                        new_url = resize_image_url(url, 150, 150)
                        images_saved.controls.append(
                            Container(content=Column(spacing=0.5,horizontal_alignment="center", controls=[Image(
                                src=new_url,
                                border_radius=10), Text(f"{loc_visited[i]['name']}", text_align="center")
                        ])))
                        page.update()
                    else:
                        print("No té foto")
            else:
                page.views.append(View(controls=[AppBar(title=Text("Historial de Llocs"), bgcolor="#AAD7D9",adaptive=True,),SafeArea(content=Text("No has explorat cap lloc encara!", text_align="center", height=page.height))], bgcolor = "#FFFCF1"))
        
        if page.route == '/configuracio/tema':
            page.add(configuracio)
            page.views.append(View(bgcolor = "#FFFCF1",controls=[AppBar(title=Text("Tema"), adaptive=True,bgcolor="#AAD7D9")]))

        if page.route == '/configuracio/idioma':
            page.add(configuracio)
            page.views.append(View(bgcolor = "#FFFCF1",controls=[AppBar(title=Text("Idioma"), adaptive=True,bgcolor="#AAD7D9")]))

        if page.route == "/configuracio/config_near":
            page.add(configuracio)
            async def radius(e):
                await page.client_storage.set_async("radius_sel", round(e.control.value) * 1000)
                radius_sel = await page.client_storage.get_async("radius_sel") 
                print(radius_sel)
            async def sort(e):
                print(e.control.value)
                if e.control.value == "Valoració":
                    await page.client_storage.set_async("sort_sel", "RATING")
                if e.control.value == "Rellevancia (default)":
                    await page.client_storage.set_async("sort_sel", "RELEVANCE")
                if e.control.value == "Distància":
                    await page.client_storage.set_async("sort_sel", "DISTANCE")
                if e.control.value == "Popularitat":
                    await page.client_storage.set_async("sort_sel", "POPULARITY")
                sort_sel = await page.client_storage.get_async("sort_sel") 
                print(sort_sel)
            async def preu_sel(e):
                await page.client_storage.set_async("preu", round(e.control.value))
                preu = await page.client_storage.get_async("preu") 
                print(preu)

            sort_sel = await page.client_storage.get_async("sort_sel")
            if sort_sel == "RATING":
                value_em = "Valoració"
            if sort_sel == "RELEVANCE":
                value_em = "Rellevancia (default)"
            if sort_sel == "DISTANCE":
                value_em = "Distància"
            if sort_sel == "POPULARITY":
                value_em = "Popularitat"
            radius_sel = await page.client_storage.get_async("radius_sel")
            print("radius_sel: ", radius_sel)
            preu = await page.client_storage.get_async("preu")
            print("preu: ", preu)
            parametres_cerca = Column([
                Divider(),
                Text("RADI, DISTÀNCIA",weight=FontWeight.W_600, size=18),
                Text("Configura la distància màxima la qual vols que cerqui l'algorisme!",weight=FontWeight.W_300),
                Slider(min=1, max=10, divisions=10, label="{value} Km", value=int(radius_sel/1000), on_change_end=radius,active_color="#7A9A9C", inactive_color="#c9d6d7"), #! No funciona el value per el async
                Divider(), 
                Text("RELLEVÀNCIA, ORDRE",weight=FontWeight.W_600, size=18),
                Text("Quins llocs t'apareixeran primer?",weight=FontWeight.W_300),
                Dropdown(
                        hint_text="Pica la teva preferencia",
                        width=page.width,
                        on_change=sort,
                        value=value_em,
                        options=[
                            dropdown.Option("Rellevancia (default)"),
                            dropdown.Option("Valoració"),
                            dropdown.Option("Distància"),
                            dropdown.Option("Popularitat")]
                ),
                Divider(),
                Text("PREU",weight=FontWeight.W_600, size=18),
                Text("Configura el preu màxim que vols pagar de l'1 al 4! 1 (barat), 4 (car). Si selecciones 0, no hi haura filtre i sortiran tots",weight=FontWeight.W_300),
                Slider(min=0, max=4, divisions=4, label="{value}", on_change_end=preu_sel,active_color="#7A9A9C", inactive_color="#c9d6d7", value=preu),
            ],scroll="adaptive")
            page.views.append(View(bgcolor = "#FFFCF1",controls=[AppBar(title=Text("Pàrametres cerca"), adaptive=True,bgcolor="#AAD7D9"),parametres_cerca]))
            
        if page.route == '/info':
            page.views.append(View(bgcolor = "#FFFCF1",controls=[AppBar(bgcolor="#AAD7D9",adaptive=True),SafeArea(content=ElevatedButton("Tornar", on_click=view_pop))]))
        
        if page.route == '/categories':
            categories_sel = page.session.get("categories_sel")
            page.add(Tags_amunt_safe,stack_cards,botons)
            Categ_info = Column([
                     ExpansionTile(
                            title=Text("Menjar",weight=FontWeight.W_600),
                            subtitle=Text("Restaurants, bars, cafeteries, etc.",weight=FontWeight.W_300),
                            affinity=TileAffinity.LEADING,
                            collapsed_text_color=colors.BLACK,
                            text_color=colors.BLACK,
                            controls=[
                                Checkbox(label="General Menjar", adaptive=True, on_change=categ_check_sel),
                                Checkbox(label="Panaderia", adaptive=True, on_change=categ_check_sel),
                                Checkbox(label="Bar", adaptive=True, on_change=categ_check_sel),
                                Checkbox(label="Cafeteria", adaptive=True, on_change=categ_check_sel),
                                Checkbox(label="Creperia", adaptive=True, on_change=categ_check_sel),
                                Checkbox(label="Botiga de postres", adaptive=True, on_change=categ_check_sel),
                                Checkbox(label="Restaurants", adaptive=True, on_change=categ_check_sel),
                                Checkbox(label="Restaurants 'Gluten-Free'", adaptive=True, on_change=categ_check_sel),
                            ],
                    ),
                     ExpansionTile(
                            title=Text("Espais naturals",weight=FontWeight.W_600),
                            subtitle=Text("Parcs, muntanyes, platges, llacs, etc.",weight=FontWeight.W_300),
                            affinity=TileAffinity.LEADING, 
                            collapsed_text_color=colors.BLACK,
                            text_color=colors.BLACK,
                            controls=[
                                Checkbox(label="General espais naturals", adaptive=True, on_change=categ_check_sel),
                                Checkbox(label="Platja", adaptive=True, on_change=categ_check_sel),
                                Checkbox(label="Monument", adaptive=True, on_change=categ_check_sel),
                                Checkbox(label="Parcs", adaptive=True, on_change=categ_check_sel),
                            ],
                    ),
                     ExpansionTile(
                            title=Text("Botigues",weight=FontWeight.W_600),
                            subtitle=Text("Botigues de roba, llibreries, centres comercials, etc.",weight=FontWeight.W_300),
                            affinity=TileAffinity.LEADING,
                            collapsed_text_color=colors.BLACK,
                            text_color=colors.BLACK,
                            controls=[
                                Checkbox(label="General Botigues", adaptive=True, on_change=categ_check_sel),
                                Checkbox(label="Roba i moda", adaptive=True, on_change=categ_check_sel),
                                Checkbox(label="Centres comercials", adaptive=True, on_change=categ_check_sel),
                                Checkbox(label="Llibreries", adaptive=True, on_change=categ_check_sel),
                                Checkbox(label="De conveniència", adaptive=True, on_change=categ_check_sel),
                                Checkbox(label="Vintage i de segona mà", adaptive=True, on_change=categ_check_sel),
                                Checkbox(label="Flors i jardins", adaptive=True, on_change=categ_check_sel),
                                Checkbox(label="Joguines", adaptive=True, on_change=categ_check_sel),
                                Checkbox(label="Menjar", adaptive=True, on_change=categ_check_sel),
                            ],
                    ),
                     ExpansionTile(
                            title=Text("Entreteniment", weight=FontWeight.W_600),
                            subtitle=Text("Inclou parcs d'atraccions, aquaris, arcades, galeries d'art, etc.", weight=FontWeight.W_300),
                            affinity=TileAffinity.LEADING,
                            collapsed_text_color=colors.BLACK,
                            text_color=colors.BLACK,
                            controls=[
                                Checkbox(label="General Entreteniment",adaptive=True, on_change=categ_check_sel),
                                Checkbox(label="Museus",adaptive=True, on_change=categ_check_sel),                                
                                Checkbox(label="Karaoke",adaptive=True, on_change=categ_check_sel),
                                Checkbox(label="Escape Room",adaptive=True, on_change=categ_check_sel),
                                Checkbox(label="Bolera", adaptive=True, on_change=categ_check_sel),
                                Checkbox(label="Cinema", adaptive=True, on_change=categ_check_sel),
                                Checkbox(label="Parc d'atraccions", adaptive=True, on_change=categ_check_sel),
                            ],
                    ),
                     ExpansionTile(
                            title=Text("Viatges",weight=FontWeight.W_600),
                            subtitle=Text("Hotels, aeroports, estacions de tren, etc.",weight=FontWeight.W_300),
                            affinity=TileAffinity.LEADING,
                            collapsed_text_color=colors.BLACK,
                            text_color=colors.BLACK,
                            controls=[
                                Checkbox(label="General viatges",adaptive=True, on_change=categ_check_sel),
                                Checkbox(label="Lloguer bicis",adaptive=True, on_change=categ_check_sel),                                
                                Checkbox(label="Lloguer de barques",adaptive=True, on_change=categ_check_sel),
                                Checkbox(label="Allotjament",adaptive=True, on_change=categ_check_sel),
                                Checkbox(label="Parking", adaptive=True, on_change=categ_check_sel),
                                Checkbox(label="Àrea de descans", adaptive=True, on_change=categ_check_sel),
                                Checkbox(label="Agència de viatges", adaptive=True, on_change=categ_check_sel),
                            ],
                    )
                    ])
            categ_info_add = Column(scroll="adaptive", height=page.height * 0.85,horizontal_alignment="center", controls=[Categ_info,ExpansionTile(
                            title=Text("Turisme",weight=FontWeight.W_600),
                            subtitle=Text("Que puc veure aqui?",weight=FontWeight.W_300),
                            affinity=TileAffinity.LEADING,
                            collapsed_text_color=colors.BLACK,
                            text_color=colors.BLACK,
                            controls=[
                                Text("Quan fas click al apartat de turisme, l'algorisme et detecta els millors llocs per visitar a prop teu!"),
                                Text("Ideal per viatges :)")
                            ],
                    ),
                    ElevatedButton("Tornar", bgcolor="#7cb7b9", color="black", on_click=view_pop)])
            
            for category in Categ_info.controls: #El que fa això es comprovar un a un si són a dins de categories_sel agafant el categories_list i agafant només el número.
                for i in range(len(category.controls)):
                    if category.controls[i].label in categories_list:
                     numeros_categ = categories_list[category.controls[i].label]
                     for numero in numeros_categ:
                        if numero in categories_sel:
                            category.controls[i].value = True #Estic feliç, funciona :D
                            category.initially_expanded=True
            page.views.append(View(bgcolor = "#FFFCF1",controls=[AppBar(title=Text("Categories"),adaptive=True, bgcolor="#AAD7D9"), SafeArea(content=categ_info_add)]))
            #page.add(AppBar(leading=IconButton(icons.ARROW_BACK_IOS,alignment="center",on_click=tornar),title=Text("Categories"), bgcolor="#AAD7D9"),categ_info_add)
            
        
        page.update()
    
    page.on_route_change = on_change_page #Aquest defineix que volem que faci el programa en el canvi de route 
    page.on_view_pop = view_pop
    
    async def seguent(e):
        cards[0].offset = transform.Offset(-4, 0)  
        page.update()
        await asyncio.sleep(0.15)  
        cards.remove(cards[0])
        print(f"Card {len(cards)} swiped left")
        await update_cards()
        await scale_next_card()
    
    async def guarda(e):
        cards[0].offset = transform.Offset(4, 0)  
        page.update()
        await asyncio.sleep(0.15)  
        cards.remove(cards[0])
        print(f"Card {len(cards)} swiped left")
        await update_cards()
        await scale_next_card()

    async def mes_info(e):
        #Animació en general per fer desapareixer tot 
        cards[0].animate_scale = animation.Animation(550)
        cards[0].scale = 2
        cards[0].opacity = 0.1
        botons.animate_opacity = animation.Animation(550)
        Tags_amunt.animate_opacity = animation.Animation(550)
        botons.opacity = 0.12
        Tags_amunt.opacity = 0.12
        page.update()
        await asyncio.sleep(0.5)
        page.controls.clear()
        page.update()
        #Comença a afegir l'altre pàgina
        page.go('/info')


    
    
    categories_list = {
        #*Chips
        "Restaurants": [13065],
        "Parcs": [16032],
        "Cafeteries": [13037],
        "Entreteniment": [10000, 12080, 17018],
        "Botigues": [17000],
        "Turisme": [10001, 10003, 10004, 10009, 16020, 10027, 16011, 16034, 16031, 16026, 16024, 16025, 16020, 16014, 16011, 16007],  # This still needs to be defined properly #! Falta fer aquest!!
        "Llocs emblematics": [16020,16026,16031,16051,16052,16053], #! Falta per concretar si esta bé
        #* General Categories
        "General Menjar":[13000],
        "General espais naturals":[16000],
        "General Botigues":[17000],
        "General Entreteniment": [10000],
        "General viatges": [19000], 
        #*Menjar
        "Panaderia": [13002],
        "Bar": [13003], 
        "Cafeteria": [13037],
        "Creperia": [13041],
        "Botiga de postres": [13040], 
        "Restaurants 'Gluten-Free": [13390],
        #*Outdoors
        "Platja": [16003],
        "Monument": [16026],
        #* Entreteniment
        "Museus": [10027],
        "Karaoke": [10021],
        "Escape Room": [10015], 
        "Bolera": [10006],
        "Cinema": [10024],
        "Parc d'atraccions": [10001,10055,10058],
        #*Viatges
        "Lloguer bicis": [19002],
        "Lloguer de barques": [19003],
        "Allotjament": [19009],
        "Parking": [19020],
        "Àrea de descans": [19024],
        "Agència de viatges": [19055],
        #*Botigues
        "Roba i moda": [17039],
        "Centres comercials":[17114,17033],
        "Llibreries":[17018,17022,12080],
        "De conveniència": [17029],
        "Vintage i de segona mà": [17138,17019],
        "Flors i jardins": [17056,17101],
        "Joguines": [17135],
        "Menjar": [17057]

    }
    def categ_check_sel(e):
        categories_sel = page.session.get("categories_sel")
        if e.control.value == True:
            categories = categories_list.get(e.control.label, [])
            for category in categories:
                if category not in categories_sel:
                    categories_sel.append(category)
                    page.session.set("categories_sel", categories_sel)
        else: 
            categories = categories_list.get(e.control.label, [])
            for category in categories:
                if category in categories_sel:
                    categories_sel.remove(category)
                    page.session.set("categories_sel", categories_sel)
        categories_sel = page.session.get("categories_sel")
        print(categories_sel)
    def categ_chip_sel(e):
        categories_sel = page.session.get("categories_sel")
        if e.control.selected:# El que fa es afegir en el cas de que estigui seleccionat i detecta la chip
            categories = categories_list.get(e.control.label.value, [])
            for category in categories:
                if category not in categories_sel:
                    categories_sel.append(category)
                    page.session.set("categories_sel", categories_sel)
        else:
            categories = categories_list.get(e.control.label.value, [])
            for category in categories:
                if category in categories_sel:
                    categories_sel.remove(category)
                    page.session.set("categories_sel", categories_sel)
        categories_sel = page.session.get("categories_sel")
        print(categories_sel)
        
    
    def mes_info_select(e):
        page.go('/categories')
        Tags_amunt.controls[len(Tags_amunt.controls) - 1].content.selected = False


#Definirem aqui tots els components com a variables per a tal d'accedir-hi en qualsevol moment en el programa
    Tags_amunt =Row( #Totes les etiquetes juntes 
                spacing=5,
                alignment= "center",
                scale=0.952,
                controls=[
                    Container(border=border.all(1, "#c4e4da"),border_radius=15.5,content=Chip(
                        selected_color="#AAD7D9",
                        bgcolor="#E8EEED",
                        label=Text("Restaurants",weight=FontWeight.W_400,font_family="default"),
                        leading=Icon(icons.RESTAURANT_MENU_OUTLINED),
                        on_select=categ_chip_sel,
                        shadow_color = "#9ebdbf",
                        selected_shadow_color = "9ebdbf",
                        elevation=2,
                        shape = RoundedRectangleBorder(radius=14.5),
                        show_checkmark=False,
                    )), 
                    Container(border=border.all(1, "#c4e4da"),border_radius=15.5,content=Chip(
                        selected_color="#AAD7D9",
                        bgcolor="#E8EEED",
                        label=Text("Llocs emblematics",weight=FontWeight.W_400,font_family="default"),
                        leading=Icon(icons.MUSEUM_OUTLINED),
                        on_select=categ_chip_sel,
                        shadow_color = "#9ebdbf",
                        selected_shadow_color = "9ebdbf",
                        elevation=2,
                        shape = RoundedRectangleBorder(radius=14.5),
                        show_checkmark=False,
                    )), 
                    Container(border=border.all(1, "#c4e4da"),border_radius=15.5,content=Chip(
                        selected_color="#AAD7D9",
                        bgcolor="#E8EEED",
                        label=Text("Parcs",weight=FontWeight.W_400,font_family="default"),
                        leading=Icon(icons.PARK_OUTLINED),
                        on_select=categ_chip_sel,
                        shadow_color = "#9ebdbf",
                        selected_shadow_color = "9ebdbf",
                        elevation=2,
                        shape = RoundedRectangleBorder(radius=14.5),
                        show_checkmark=False,
                    )), 
                    Container(border=border.all(1, "#c4e4da"),border_radius=15.5,content=Chip(
                        selected_color="#AAD7D9",
                        bgcolor="#E8EEED",
                        label=Text("Cafeteries",weight=FontWeight.W_400,font_family="default"),
                        leading=Icon(icons.LOCAL_CAFE_OUTLINED),
                        on_select=categ_chip_sel,
                        shadow_color = "#9ebdbf",
                        selected_shadow_color = "9ebdbf",
                        elevation=2,
                        shape = RoundedRectangleBorder(radius=14.5),
                        show_checkmark=False,
                    )), 
                    Container(border=border.all(1, "#c4e4da"),border_radius=15.5,content=Chip(
                        selected_color="#AAD7D9",
                        bgcolor="#E8EEED",
                        label=Text("Entreteniment",weight=FontWeight.W_400,font_family="default"),
                        leading=Icon(icons.INSERT_EMOTICON_OUTLINED),
                        on_select=categ_chip_sel,
                        shadow_color = "#9ebdbf",
                        selected_shadow_color = "9ebdbf",
                        elevation=2,
                        shape = RoundedRectangleBorder(radius=14.5),
                        show_checkmark=False,
                    )), 
                    Container(border=border.all(1, "#c4e4da"),border_radius=15.5,content=Chip(
                        selected_color="#AAD7D9",
                        bgcolor="#E8EEED",
                        label=Text("Botigues",weight=FontWeight.W_400,font_family="default"),
                        leading=Icon(icons.SHOPPING_BAG_OUTLINED),
                        on_select=categ_chip_sel,
                        shadow_color = "#9ebdbf",
                        selected_shadow_color = "9ebdbf",
                        elevation=2,
                        shape = RoundedRectangleBorder(radius=14.5),
                        show_checkmark=False,
                    )), 
                    Container(border=border.all(1, "#c4e4da"),border_radius=15.5,content=Chip(
                        selected_color="#AAD7D9",
                        bgcolor="#E8EEED",
                        label=Text("Turisme",weight=FontWeight.W_400,font_family="default"),
                        leading=Icon(icons.FLIGHT_OUTLINED),
                        on_select=categ_chip_sel,
                        shadow_color = "#9ebdbf",
                        selected_shadow_color = "9ebdbf",
                        elevation=2,
                        shape = RoundedRectangleBorder(radius=14.5),
                        show_checkmark=False,
                    )), 
                    Container(border=border.all(1, "#829891"),border_radius=15.5,content=Chip(
                        selected_color="#AAD7D9",
                        bgcolor="#E8EEED",
                        label=Text("Més",weight=FontWeight.W_400,font_family="default"),
                        leading=Icon(icons.READ_MORE_OUTLINED,color="black"),
                        on_select=mes_info_select,
                        shadow_color = "#9ebdbf",
                        selected_shadow_color = "9ebdbf",
                        elevation=2,
                        shape = RoundedRectangleBorder(radius=14.5),
                        show_checkmark=False,
                    )), 
                ],
                scroll="adaptive", # ! Canviar a hidden quan facis la build
    )
    size_botons = page.width / 30
    if size_botons >= 14:
        size_botons = 14
    botons = ResponsiveRow( #Aqui van tots els botons junts 
            vertical_alignment="end",
            controls=[
                ElevatedButton(content=Text("Següent", size=size_botons, theme_style=TextThemeStyle.LABEL_LARGE),on_click=seguent, bgcolor="#d9acaa", color="black",col=4), 
                ElevatedButton(content=Text("Més info",size=size_botons,theme_style=TextThemeStyle.LABEL_LARGE), on_click=mes_info,bgcolor="#FBF9F1",color="black",col=4),
                ElevatedButton(content=Text("Guarda!",size=size_botons, theme_style=TextThemeStyle.LABEL_LARGE), on_click=guarda, bgcolor="#aad9c4",color="black",col=4), 
    ]) 
    stack_cards = Stack(alignment=alignment.center, offset=(0,0), expand = True)
    saved_cards = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25] # Suposem que tenim ja la variable i la deixem 
    images_saved = GridView(
        expand=True,
        height=page.height * 0.89, 
        runs_count=3,
        child_aspect_ratio=1,
        spacing=25,
        run_spacing=5
    )
    
    async def tema(e):
        page.go('/configuracio/tema')
    async def Historial(e):
        page.go("/configuracio/historial")
    async def Idioma(e):
        page.go("/configuracio/idioma")
    async def config_near(e):
        page.go("/configuracio/config_near")
    configuracio =Card(color = "#AAD7D9", height=page.height * 0.8, expand=True,
            content=Container(
                content=Column(
                    [
                        ListTile(
                            title=Text("Configuració", theme_style=TextThemeStyle.HEADLINE_SMALL, weight=FontWeight.W_500),
                            height=(page.height * 0.8) / 13,
                        ),
                        ListTile(title=Text("General"), dense=True,height=(page.height * 0.8) / 10),
                        ListTile(
                            leading=Icon(icons.PALETTE_OUTLINED, color="black"),
                            trailing = Icon(icons.CHEVRON_RIGHT_OUTLINED),
                            title=Text("Tema", color="black"),
                            selected=True,
                            height=(page.height * 0.8) / 13,
                            on_click=tema
                        ),
                        ListTile(
                            leading=Icon(icons.LANGUAGE, color="black"),
                            trailing = Icon(icons.CHEVRON_RIGHT_OUTLINED),
                            title=Text("Idioma", color="black"),
                            selected=True,
                            height=(page.height * 0.8) / 13,
                            on_click=Idioma
                        ),
                        ListTile(
                            leading=Icon(icons.HISTORY, color="black"),
                            trailing = Icon(icons.CHEVRON_RIGHT_OUTLINED),
                            title=Text("Historial de llocs", color="black"),
                            selected=True,
                            height=(page.height * 0.8) / 13,
                            on_click=Historial
                        ),
                        ListTile(
                            leading=Icon(icons.NEAR_ME_OUTLINED, color="black"),
                            trailing = Icon(icons.CHEVRON_RIGHT_OUTLINED),
                            title=Text("Pàrametres cerca de llocs", color="black"),
                            selected=True,
                            height=(page.height * 0.8) / 13,
                            on_click=config_near
                        ),
                        ListTile(title=Text("Jo i l'App"), dense=True,height=(page.height * 0.8) / 10),
                        ListTile(
                            leading=Icon(icons.INFO_OUTLINED, color="black"),
                            trailing = Icon(icons.CHEVRON_RIGHT_OUTLINED),
                            title=Text("Sobre l'App", color="black"),
                            height=(page.height * 0.8) / 13,
                            selected=True,
                            # on_click=hey
                        ),
                        ListTile(
                            leading=Icon(icons.PRIVACY_TIP_OUTLINED, color="black"),
                            trailing = Icon(icons.CHEVRON_RIGHT_OUTLINED),
                            title=Text("Politica de privacitat", color="black"),
                            selected=True,
                            height=(page.height * 0.8) / 13,
                            # on_click=hey
                        ),
                        ListTile(
                            leading=Icon(icons.HELP_OUTLINED, color="black"),
                            trailing = Icon(icons.CHEVRON_RIGHT_OUTLINED),
                            title=Text("Ajuda", color="black"),
                            selected=True,
                            height=(page.height * 0.8) / 13,
                            # on_click=hey
                        ),
                    ],
                    spacing=0,
                ),
            )
        )

    configuracio = SafeArea(content=configuracio)

    async def changetab(e):
        index = e.control.selected_index
        if index == 1: #Llocs
            page.go('/')
            await asyncio.sleep(0.001)
            selected_llocs.offset = transform.Offset(0, -0.25)
            page.update()
            await asyncio.sleep(0.14)
            selected_llocs.offset = transform.Offset(0,0)
            
            
        elif index == 0: #Favorits
            page.go('/favorits')
            while index == 0: #Animacions icones
                await asyncio.sleep(1)
                selected_favorits.size = 27 if selected_favorits.size == 24 else 24
                page.update()
                index = e.control.selected_index #S'ha d'actualitzar a dins del codi la variable index, ja que sinó sempre sera True

        elif index == 2: #Configuració
            page.go('/configuracio')
            await asyncio.sleep(0.001)
            selected_configuracio.rotate.angle += (2*pi)
            page.update()
            
             
        page.update()
    
    selected_favorits =Icon(name=icons.FAVORITE_ROUNDED, color="#E78895", animate_size=200)
    selected_llocs =Icon(name=icons.LOCATION_PIN, color=colors.BLACK, animate_offset=140, offset=transform.Offset(0,0)) 
    selected_configuracio = Icon(name=icons.SETTINGS_ROUNDED, color=colors.BLACK, rotate=transform.Rotate(0, alignment=alignment.center), animate_rotation=animation.Animation(duration=1000, curve="bounceOut"))
    
    page.navigation_bar=NavigationBar(
        bgcolor = "#7cb7b9",
        selected_index = 1,
        indicator_color = "#FBF9F1",
        on_change=changetab,
        destinations=[
            NavigationBarDestination(label="Favorits", icon="FAVORITE_BORDER_ROUNDED", selected_icon_content=selected_favorits),
            NavigationBarDestination(label="Llocs", icon="LOCATION_ON_OUTLINED", selected_icon_content=selected_llocs), 
            NavigationBarDestination(label="Configuració", icon="SETTINGS_OUTLINED", selected_icon_content=selected_configuracio),
        ]
    )
    
    botons.height = page.height * 0.08
    botons.width = page.width
    page.navigation_bar.height = page.height * 0.11
    Tags_amunt.height = page.height * 0.045
    Tags_amunt.width = page.width 
    stack_cards.height = page.height * 0.8
    stack_cards.width = page.width 
   
    async def on_swipe(e):
        data = json.loads(e.data)
        print(data["pv"])
        if data["pv"] != 0:
            if data["pv"] < 1: #Esquerra
                await seguent(e)
            elif data["pv"] > 0: #Dreta
                await guarda(e)

    async def on_swipe_vertical(e):
        data = json.loads(e.data)
        print(data["pv"])
        if data["pv"] < 1 and data["vy"] < 0:
            await mes_info(e)
            
    
    # Aquest el que fa es convertir cada card individual en GestureDetector. Amb això, podem detectar cap a on es mou i com funciona. Es molt útil i ens ho serà en un futur.
    async def update_cards():
        stack_cards.controls.clear() 
        global index_photo_stack
        global images_request #! Variable local de sessió, també guardada dins de l'app
        global canvi
        global cards
        #:) Solucionat tot emmagatzemat!!!!!!!!
        loc_visited = await page.client_storage.get_async("loc_visited") 
        categories_sel = page.session.get("categories_sel")
        categories_sel_antic = page.session.get("categories_sel_antic")
        print("categories_sel_antic:",categories_sel_antic)
        print("categories_sel:",categories_sel)
        if categories_sel_antic != categories_sel:
            canvi = True
            print("CANVIIII!")
        categories_sel_antic = copy.deepcopy(categories_sel) 
        categories_sel_antic = page.session.set("categories_sel_antic", categories_sel_antic)

        sort_sel = await page.client_storage.get_async("sort_sel")
        radius_sel = await page.client_storage.get_async("radius_sel")
        preu = await page.client_storage.get_async("preu")
        
        print("sort_sel:", sort_sel)
        print("categories_sel:",categories_sel)
        print("radius_sel:",radius_sel)
        #print("loc_visited:",loc_visited)
        print("Preu:", preu)
        
        if len(cards) == 0 or canvi == True:
                #* Demanem les dades 
                print("index_photo_Stack: ",index_photo_stack)
                if canvi == True:
                    canvi = False
                    loc_visited = loc_visited[:index_photo_stack]
                    print(len(loc_visited))
                    dadesLlocs = []
                    cards.clear()
                    await page.client_storage.set_async("loc_visited", loc_visited)
                
                index_photo_stack = -1
                #:) Cobren el mateix demanant 5, 10 que 50
                p = await gl.get_current_position_async()
                llocs = Llocs(p.latitude,p.longitude,radius_sel,25,loc_visited,categories_sel,sort_sel, preu) #! Problema, dona sempre el mateix BUG-5

                dadesLlocs, loc_visited = llocs.dades()
                await page.client_storage.set_async("loc_visited", loc_visited)

                if dadesLlocs == []:
                    print("Això no ha de passar!") 
                images_request = llocs.photos()
                await page.client_storage.set_async("loc_visited_photos", images_request)
                # images_request = [['https://fastly.4sqi.net/img/general/1440x1920/209508005_xmMcJH4864s7dccOvwmqexKLSM5pRz-54a_-ZY28VQQ.jpg'], [], ['https://fastly.4sqi.net/img/general/1440x1440/1155361_-97JsI0c31PcZvsN0xSPzpTpa1olyfg8HgejN5Qc9kA.jpg', 'https://fastly.4sqi.net/img/general/1080x1440/63332301_OPSQur0wEPIInNCGA5i_6O9wxlJMkye6eNe9yu_3g_E.jpg', 'https://fastly.4sqi.net/img/general/1920x1440/63317963_YkZxzfAODCt0Omem-bebdXodQRXZtelyRVttYnORt00.jpg', 'https://fastly.4sqi.net/img/general/1920x1440/79698049__J7fW0S327ZmgJBW8kJFzjxwnkTsR-7-n70M2cCxEmM.jpg', 'https://fastly.4sqi.net/img/general/1440x1920/79698049_Yf7vPQi1eWtB-b_NsQtgamd9JvbVBro5gsdtOIb4dME.jpg'], ['https://fastly.4sqi.net/img/general/1440x1920/10297454_P7H9DLKojEyyA6FwEarbih8hUDk1iYCrZpPV-XXAngE.jpg', 'https://fastly.4sqi.net/img/general/2988x5312/72324205_BBP16AvGCkkPEa-BvcRAdDPP4ZkbvDRAUTvEMOWAvZA.jpg', 'https://fastly.4sqi.net/img/general/5312x2988/72324205_DcDNsjmSLQ3-ZUlLl9cuRQJKy43bapzpQjgT3LskzkU.jpg', 'https://fastly.4sqi.net/img/general/1432x1920/26910369_gblcczWZkoG6NO4rAUMMFWZsCA7V6wTR3VXJtpCFx_U.jpg'], ['https://fastly.4sqi.net/img/general/1920x1440/11012402_OOtLuREQ5psxuxT1XZF8NEpqLfKyOuhIBixABXlMiX8.jpg', 'https://fastly.4sqi.net/img/general/1920x1440/11012402_jFOLsDCj2E7AFh30KeUV35OvOkiFH6yFC8locE9K9t0.jpg', 'https://fastly.4sqi.net/img/general/1920x1440/11012402_qvvIeZJ9gdrBmxd6jqUbgJODwiwGY_b72PVd0TPd0mE.jpg', 'https://fastly.4sqi.net/img/general/1440x1920/3498714_wGI4uZC8Z7BZA5zvCNXsZzsZcigOOIrmXSelSrIKHzs.jpg', 'https://fastly.4sqi.net/img/general/1919x1121/48025561_LciG6NtJXoZga3JsCez2wl3Z-NvvpGS0A9XNojpivMk.jpg'], ['https://fastly.4sqi.net/img/general/1920x1440/1155361_CMghvt2Z0se0A1cplhofBX75fVb9f7QAXmr0Dndt-1c.jpg', 'https://fastly.4sqi.net/img/general/1920x1440/1155361_YoSYNbWD0jWfN3kBTpCI6PUnSt3mXVYzmrn6DDramIQ.jpg', 'https://fastly.4sqi.net/img/general/1440x1920/54053478_ujB1-DAIq6iQ694cJAMVxqxL3VKw3QP3czH9o8TAGjg.jpg', 'https://fastly.4sqi.net/img/general/1920x1440/20522136_mYP0kKgJgRr4YO_7eS9gTleeMyFugt_IOjRnXjarRHQ.jpg', 'https://fastly.4sqi.net/img/general/1440x1920/12767036_ixCc2llOklbMy7hdtq2O3ukhXbCKF1JNIQVUSU9AhFc.jpg'], ['https://fastly.4sqi.net/img/general/1920x1440/23910712_1_duUH8czk_5ktvoIDFVSgcCcPIwc9g1kYGtsn-YZ_4.jpg', 'https://fastly.4sqi.net/img/general/1920x1440/23910712_Un2WyBHEKW967_HQ3IBrQDVTGLjJ4UItn4AiTT1f6bA.jpg', 'https://fastly.4sqi.net/img/general/1440x1920/23910712_6jeQ-I23iztTYeFBkAhiue_k3E5gfawJzbNLzuxAbm8.jpg', 'https://fastly.4sqi.net/img/general/1440x1920/79041888_t3HpbQG7SB_zJH3VaEnzPmSnMcYm6EZFjkt11UDokCE.jpg'], ['https://fastly.4sqi.net/img/general/1816x2993/8567928_3zgRBNoZNT1Cjclupr-nUkDtEblI9GTHGKL1CEC2z1Q.jpg', 'https://fastly.4sqi.net/img/general/1816x2945/8567928_PNfxVhBJ836oGXyEIlPqbsLeo1X7u4LfLJI2aCPZH9U.jpg', 'https://fastly.4sqi.net/img/general/1088x2304/8567928_NW64pN-n2msJ07VK4jOjtnwed4-BY_M5u-vPjLLrYZs.jpg', 'https://fastly.4sqi.net/img/general/1728x2304/8567928_dmaOyUPsGE4Few1bYbd1Otk2ipDLPnx0qWQ-mXApsF0.jpg', 'https://fastly.4sqi.net/img/general/1500x2000/8567928_qoMXxwQGZjM09AKh-hJZ8xABPLinA2Lfyb6RKGACA-c.jpg'], ['https://fastly.4sqi.net/img/general/1440x1920/67909_g6Ik7Afc5DLtftGtyGeMNTyMYxkF7fkrKchUAlk9yRk.jpg', 'https://fastly.4sqi.net/img/general/1440x1920/88652692_MZYjBb89PNxB6SU8y3G7MYGVnvJ3uJq3W8a8Q8HZCRY.jpg', 'https://fastly.4sqi.net/img/general/1440x1920/328094992_yb2PZiF7EONf_1e-mf5MjtHPYW-pONtziks1chvG9Zs.jpg', 'https://fastly.4sqi.net/img/general/1920x1440/89376305_XW011nNjuEDdyOSXoTIAJPkHVj24t-ozeF4t04Olokw.jpg', 'https://fastly.4sqi.net/img/general/1920x1440/2462338_W7zBsoS2s8tBiiIdTBwUSiliuBUYGwgrCDNslliqMTo.jpg'], ['https://fastly.4sqi.net/img/general/4032x3024/11191832_VTp_tkBb6sDP6jGuqQiGLkm_cBS_SIb7UIxFSG7xoa4.jpg', 'https://fastly.4sqi.net/img/general/1500x2000/11191832_FFseIiQA_zXJEA9BmWLeg2id_hBFMO-es21LcjGBQJo.jpg', 'https://fastly.4sqi.net/img/general/1440x1920/5116689_AYUVMJUjvmB5FcSO-XTqmgQ3sPADB6Igft7Ep4JChLU.jpg', 'https://fastly.4sqi.net/img/general/1440x1920/1817856_ZNVmoO83rDyIQoKLi_4jtJayprPxkHC3v7L8mM4fP7Y.jpg', 'https://fastly.4sqi.net/img/general/960x720/7835341_cNL6lUvIs2cfe9S5Q6H_M7KFnIryE7r4ZD08Ny_yqxM.jpg']]
                # print(images_request)
                categories = llocs.categories()
                #categories = [['https://ss3.4sqi.net/img/categories_v2/food/bbqalt_120.png', 'https://ss3.4sqi.net/img/categories_v2/food/burger_120.png', 'https://ss3.4sqi.net/img/categories_v2/food/fastfood_120.png'], ['https://ss3.4sqi.net/img/categories_v2/food/mediterranean_120.png'], ['https://ss3.4sqi.net/img/categories_v2/food/coffeeshop_120.png', 'https://ss3.4sqi.net/img/categories_v2/food/icecream_120.png', 'https://ss3.4sqi.net/img/categories_v2/food/default_120.png'], ['https://ss3.4sqi.net/img/categories_v2/food/pizza_120.png', 'https://ss3.4sqi.net/img/categories_v2/food/fastfood_120.png', 'https://ss3.4sqi.net/img/categories_v2/food/deli_120.png'], ['https://ss3.4sqi.net/img/categories_v2/food/middleeastern_120.png', 'https://ss3.4sqi.net/img/categories_v2/food/turkish_120.png'], ['https://ss3.4sqi.net/img/categories_v2/parks_outdoors/beach_120.png'], ['https://ss3.4sqi.net/img/categories_v2/nightlife/pub_120.png'], ['https://ss3.4sqi.net/img/categories_v2/nightlife/pub_120.png', 'https://ss3.4sqi.net/img/categories_v2/food/default_120.png'], ['https://ss3.4sqi.net/img/categories_v2/food/bakery_120.png'], ['https://ss3.4sqi.net/img/categories_v2/food/deli_120.png']]
                # print(categories)

                for i in range(len(dadesLlocs)):
                    print("dadesLlocs i", i)
                    # Definim tots els components de la card
                    if 'address' in dadesLlocs[i]["location"]: #! BUG-6
                        subtitle_card = Column(horizontal_alignment="center", controls=[
                            Text(f"Direcció: {dadesLlocs[i]['location']['address']} | Distància: {dadesLlocs[i]['distance']}m", color="white", weight=FontWeight.W_900),
                            Row(alignment="center",width = page.width, controls=[])
                            ]) #! Fer que sigui responsive row per si la pantalla es més petita
                    else: 
                        subtitle_card = Column(horizontal_alignment="center", controls=[
                            Text(f"Direcció: {None} | Distància: {dadesLlocs[i]['distance']}m", color="white",weight=FontWeight.W_900),
                            Row(alignment="center",width = page.width, controls=[])
                            ]) 
                    for j in range(len(categories[i])):
                        subtitle_card.controls[1].controls.append(
                            Image(src=categories[i][j], height=20)
                    )
                    
                    def get_dynamic_font_size(text, base_size, min_size, max_size):
                        text_length = len(text)
                        if text_length <= 10:
                            return max_size
                        elif text_length >= 50:
                            return min_size
                        else:
                            return max_size - (max_size - min_size) * (text_length - 10) / (50 - 10)

                    # Example base size, minimum size, and maximum size
                    base_size = page.height * 0.055
                    min_size = 8
                    max_size = base_size - 13

                    # Adjust size_title based on the length of dadesLlocs[i]["name"]
                    size_title = get_dynamic_font_size(dadesLlocs[i]["name"], base_size, min_size, max_size) # :) Mig solucionat
                    #size_title = (page.height * 0.055) - 10 #! BUG-7
                    nom_del_restaurant = Stack(
                            alignment=alignment.center,
                            height=page.height * 0.055,
                            width=page.width,
                            controls=[
                                Container(
                                    content=Text(
                                        no_wrap = True,
                                        text_align="center", 
                                        width=page.width,
                                        height=page.height * 0.12,
                                        spans=[
                                            TextSpan(
                                                f"{dadesLlocs[i]['name']}",  
                                                TextStyle(
                                                    weight=FontWeight.W_900,
                                                    size=size_title,
                                                    font_family="WorkSans",
                                                    foreground=Paint(
                                                        color="#FFFFEA",
                                                        stroke_width=3.4,
                                                        stroke_join=StrokeJoin.BEVEL,
                                                        style=PaintingStyle.STROKE,
                                                    ),
                                                ),
                                            ),
                                        ],
                                    ),
                                    alignment=alignment.center
                                ),
                                Container(
                                    content=Text(
                                        no_wrap = True,
                                        text_align="center",
                                        width=page.width,
                                        height=page.height * 0.12,
                                        spans=[
                                            TextSpan(
                                                f"{dadesLlocs[i]["name"]}",
                                                TextStyle( 
                                                    size=size_title,
                                                    weight=FontWeight.W_900,
                                                    font_family="WorkSans",
                                                    color=colors.BLACK,
                                                ),
                                            ),
                                        ],
                                    ),
                                    alignment=alignment.center
                                ),
                            ],
                        )
 
                    print("images_request i", images_request[i])
                    print("index_photo_stack", index_photo_stack)

                    if images_request[i] != []: #! BUG-6
                        print("Si té fotos")
                        if len(dadesLlocs[i]['photos']) == 1: 
                            print("prova")
                            img_principal = Row(alignment="center",controls=[AnimatedSwitcher(transition=AnimatedSwitcherTransition.FADE,duration=500,content=Image(
                                    animate_opacity=200,
                                    border_radius=15,
                                    src=images_request[i][0], #URL imatge
                                    width = page.width * 0.8, 
                                    height = page.height * 0.8 * 0.65, 
                                    fit="COVER"
                                    ))])
                            img_esq =Image(
                                        animate_opacity=200,
                                        left=-page.width * 0.75,
                                        top=35,                                    
                                        border_radius=20,
                                        width = page.width * 0.8, 
                                        height = page.height * 0.8 * 0.55, 
                                        fit="COVER",
                                    )
                            img_dret = Image(
                                        animate_opacity=200,
                                        right=-page.width * 0.75,
                                        top=35,
                                        border_radius=15,
                                        width = page.width * 0.8, 
                                        height = page.height * 0.8 * 0.55, 
                                        fit="COVER",
                                    )
                        else: 
                                img_principal = Row(alignment="center",controls=[AnimatedSwitcher(transition=AnimatedSwitcherTransition.FADE,duration=500,content=Image(
                                    animate_opacity=200,
                                    border_radius=15,
                                    src=images_request[i][0], #URL imatge
                                    width = page.width * 0.8, 
                                    height = page.height * 0.8 * 0.65, 
                                    fit="COVER"
                                    ))])
                                img_esq =Image(
                                        animate_opacity=200,
                                        left=-page.width * 0.75,
                                        top=35,                                     # ! BUG-8
                                        src=images_request[i][len(images_request[i]) - 1],#URL imatge
                                        border_radius=20,
                                        width = page.width * 0.8, 
                                        height = page.height * 0.8 * 0.55, 
                                        fit="COVER",
                                    )
                                img_dret = Image(
                                        animate_opacity=200,
                                        right=-page.width * 0.75,
                                        top=35,
                                        src=images_request[i][1],#URL imatge
                                        border_radius=15,
                                        width = page.width * 0.8, 
                                        height = page.height * 0.8 * 0.55, 
                                        fit="COVER",
                                    )
                    else:
                        img_principal = Row(alignment="center",controls=[AnimatedSwitcher(transition=AnimatedSwitcherTransition.FADE,duration=500,content=Image(
                                    animate_opacity=200,
                                    border_radius=15,
                                    width = page.width * 0.8, 
                                    height = page.height * 0.8 * 0.65, 
                                    fit="COVER"
                                    ))])
                        img_esq =Image(
                                        animate_opacity=200,
                                        left=-page.width * 0.75,
                                        top=35,                                     # ! BUG-8
                                        border_radius=20,
                                        width = page.width * 0.8, 
                                        height = page.height * 0.8 * 0.55, 
                                        fit="COVER",
                                    )
                        img_dret = Image(
                                        animate_opacity=200,
                                        right=-page.width * 0.75,
                                        top=35,
                                        border_radius=15,
                                        width = page.width * 0.8, 
                                        height = page.height * 0.8 * 0.55, 
                                        fit="COVER",
                                    )
                        print("No té fotos")
 
                    
                    async def esq(e): #Detecta que has fet click a l'esquerra 
                        global index_photo
                        img_principal = stack_cards.controls[0].content.content.controls[1].content.controls[0].controls[0].content
                        img_dret = stack_cards.controls[0].content.content.controls[1].content.controls[2]
                        img_esq = stack_cards.controls[0].content.content.controls[1].content.controls[1]
                        if index_photo <= 0:
                                index_photo = len(images_request[index_photo_stack]) - 1 # Fa que sempre l'index sigui un número a dins de la llista i resta un, fent així que puguem navegar
                        else:
                            index_photo -= 1
                        img_principal.opacity = 0.1 #Animació d'opactiat, perquè l'usuari tingui més comoditat visual 
                        img_principal.update()
                        await asyncio.sleep(0.2) 
                        img_principal.src = images_request[index_photo_stack][index_photo] #Actualitza les fotos 
                        img_principal.opacity = 1
                        img_esq.src = images_request[index_photo_stack][index_photo-1 if index_photo-1 >= 0 else (len(images_request[index_photo_stack])-1)]  #Resta un en el cas que sigui a dins de la llista, sinó posa el més gran (len) - 1, ja que contem des de 0
                        #Incís: Mai entendre perquè els programadors contem des de 0, i després quan fas la longitud d'una llista conta des de 1, en fi.
                        img_dret.src = images_request[index_photo_stack][index_photo+1 if index_photo+1 <= (len(images_request[index_photo_stack])- 1) else 0] #El mateix, detecta que sigui a dins de la llista i no sigui negatiu, en el cas posa 0
                        page.update()
                    async def dret(e): #Mateixos comentaris pero al reves
                        global index_photo
                        img_principal = stack_cards.controls[0].content.content.controls[1].content.controls[0].controls[0].content
                        img_dret = stack_cards.controls[0].content.content.controls[1].content.controls[2]
                        img_esq = stack_cards.controls[0].content.content.controls[1].content.controls[1]
                        if index_photo >= (len(images_request[index_photo_stack])- 1):
                            index_photo = 0
                        else:
                            index_photo += 1
                        img_principal.opacity = 0.1 #Animació d'opactiat, perquè l'usuari tingui més comoditat visual 
                        img_principal.update()
                        await asyncio.sleep(0.2) 
                        img_principal.src = images_request[index_photo_stack][index_photo] 
                        img_principal.opacity = 1
                        img_esq.src = images_request[index_photo_stack][index_photo-1 if index_photo-1 >= 0 else (len(images_request[index_photo_stack])-1)]  
                        img_dret.src = images_request[index_photo_stack][index_photo+1 if index_photo+1 <= (len(images_request[index_photo_stack])- 1) else 0]  
                        page.update()
                    
                    print("Carta creada")
                    carta = Container(
                            image_src = "src/fons.jpg", #! Canviar-la a l'assets
                            image_fit = "FILL",
                            offset=(0,0),
                            border_radius=15, 
                            width = page.width,
                            height = page.height * 0.8,
                            animate_offset=animation.Animation(500),
                            animate_opacity = animation.Animation(600),
                            scale=0,
                            animate_scale=animation.Animation(340, "easeOutSine"),
                            content=Column(
                                horizontal_alignment="center",
                                controls=[
                                    ListTile(
                                        title=nom_del_restaurant,
                                        subtitle=subtitle_card,
                                        height=(page.height * 0.8) * 0.15  
                                        ),
                                        Container(content=Stack(
                                                        [   img_principal,
                                                            img_esq,
                                                            img_dret,
                                                            IconButton(
                                                                    icon=icons.CHEVRON_RIGHT,
                                                                    icon_color = "black",
                                                                    bgcolor="#FBF9F1",
                                                                    on_click=lambda e: asyncio.run(esq(e)),
                                                                    alignment=alignment.center,
                                                                    right=2,
                                                                    width = page.window.width * 0.1,
                                                                    top=page.window.height * 0.8 * 0.7 / 2,
                                                            ),
                                                            IconButton(
                                                                    icon=icons.CHEVRON_LEFT,
                                                                    icon_color = "black",
                                                                    bgcolor="#FBF9F1",
                                                                    on_click=lambda e: asyncio.run(dret(e)),
                                                                    width = page.window.width * 0.1,
                                                                    left=2,
                                                                    top=page.window.height * 0.8 * 0.7 / 2,
                                                            ),
                                                        ]
                                                    ),
                                                    # expand_loose=True,
                                                    width=page.width,
                                                    height=page.height * 0.8 * 0.6,
                                                ),
                                                Row([],width = page.width, alignment="center")
                                    ]
                                )
                                        
                        )
                    cards.append(carta)
                    
                    if 'rating' in dadesLlocs[i]: #! BUG-6
                        bottom_rating = Text(f"Rating: {dadesLlocs[i]['rating']}", color="white", weight=FontWeight.W_900)
                        carta.content.controls[2].controls.append(bottom_rating)
                    if 'price' in dadesLlocs[i]: #! BUG-6
                        bottom_price = Row([Text(f"Price (màx 4): ",color="white",weight=FontWeight.W_900)])
                        for c in range(round(dadesLlocs[i]['price'])):
                            if dadesLlocs[i]['price'] == 1:
                                color = "#b4deb6" 
                            elif dadesLlocs[i]['price'] == 2:
                                color = "#ffffbf"
                            elif dadesLlocs[i]['price'] == 3:
                                color = "#ffc08c"
                            else:
                                color = "#ff7b5a"
                            bottom_price.controls.append(
                                Icon(icons.ATTACH_MONEY, color=color)
                            )  
                        carta.content.controls[2].controls.append(bottom_price)

                page.update()   

        first_card_added = False

        for card in cards:
            if not first_card_added:
                print("Carta insertada")
                index_photo_stack += 1
                print("index_photo_stack", index_photo_stack)
                stack_cards.controls.append(
                    GestureDetector(
                        content=card,
                        on_horizontal_drag_end=on_swipe,
                        on_vertical_drag_end=on_swipe_vertical
                    )
                ) #! BUG-3   
                # :) Solucionat!
                img_principal = stack_cards.controls[0].content.content.controls[1].content.controls[0].controls[0].content     
                img_principal_animate = stack_cards.controls[0].content.content.controls[1].content.controls[0]
                img_dret = stack_cards.controls[0].content.content.controls[1].content.controls[2]
                img_esq = stack_cards.controls[0].content.content.controls[1].content.controls[1]
                #Definim tambè els botons 
                IconButton_dret = stack_cards.controls[0].content.content.controls[1].content.controls[3]
                IconButton_esq = stack_cards.controls[0].content.content.controls[1].content.controls[4]
                img_principal.visible = True
                img_dret.visible = True
                img_esq.visible = True
                IconButton_dret.visible = True
                IconButton_esq.visible = True

                if len(images_request[index_photo_stack]) > 1:
                    img_principal.src = images_request[index_photo_stack][0]
                    img_dret.src = images_request[index_photo_stack][1] 
                    img_esq.src = images_request[index_photo_stack][len(images_request[index_photo_stack]) - 1]
                    page.update()
                elif len(images_request[index_photo_stack]) == 1:
                    print("es 1")
                    img_principal.src = images_request[index_photo_stack][0]
                    img_dret.visible = False
                    img_esq.visible = False
                    IconButton_dret.visible = False
                    IconButton_esq.visible = False
                elif len(images_request[index_photo_stack]) == 0:
                    IconButton_dret.visible = False
                    IconButton_esq.visible = False
                    img_principal_animate.visible = False
                    img_dret.visible = False
                    img_esq.visible = False # * Com a proposta pots posar un embed del maps!
                page.update()

                first_card_added = True
            else:
                break

 
    
    await update_cards()
    
    #L'iniciem només començar el programa per tal de fer apareixer tots els elements i escalem la primera a 1 per tal de mostrar-la
    
    async def scale_next_card():
        global images_request
        global index_photo_stack
        if len(cards) >= 1:  
            next_card = cards[0]
            next_card.scale = 0
            page.update()
            await asyncio.sleep(0.35)  
            next_card.scale = 1
            page.update()

    Tags_amunt_safe = SafeArea(content=Tags_amunt)
    page.add(
        Tags_amunt_safe,
        stack_cards,
        botons, 
    )
    await scale_next_card()
    
    
flet.app(target=main,assets_dir="assets")