import flet 
from flet import Page,Dropdown,dropdown,Divider,View,border,Slider,Checkbox,RoundedRectangleBorder,TileAffinity,ExpansionTile,Geolocator,AnimatedSwitcherTransition,AppBar,Card,GridView,TextThemeStyle,ListTile, MainAxisAlignment,AnimatedSwitcher,Stack,Column,TextSpan,TextStyle,Paint,AlertDialog,IconButton, StrokeJoin,PaintingStyle,ShadowBlurStyle, BoxShadow, Image, ListTile,GestureDetector, FontWeight,ElevatedButton, SafeArea,Theme, animation, Container, transform, Icon, icons, colors, alignment, icons, Row, Text, ResponsiveRow, Chip, NavigationBarDestination, NavigationBar 
from math import pi
import asyncio
import json
import location
index_photo = 0
import requests
import random

loc_visited = []
images_request = []
index_photo_stack = -1
class Llocs:
    def __init__(self, latitud, longitud, radius, limit, loc_visited,categories_sel, sort_sel): #Definim totes les variables que hem donat a traves de la class
        self.latitud = latitud 
        self.longitud = longitud
        self.radius = radius
        self.limit = limit
        self.loc_visited = loc_visited
        self.categories_s = categories_sel
        self.sort = sort_sel

    def _randomize_coordinates(self, lat, lon):
        # Afegeix un petit desplaçament a les coordenades perquè no sigui sempre igual
        print(len(loc_visited))
        increment = len(self.loc_visited) / 1000
        print("increment és:", increment)
        if len(self.loc_visited) > 1 and len(self.loc_visited) < 10: #Aquest el que fa es detectar la longitud de les places ja visitades i depenent d'aquesta fa més variació o menys
            randloc = (len(self.loc_visited) // 10) * increment
        elif len(self.loc_visited) >= 10: 
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
    #gl = Geolocator()
    #page.add(gl)
    #gl.request_permission() 
    #location.handle_permission(gl,AlertDialog, page, Text,TextButton,MainAxisAlignment)
    page.update()
    page.session.set("categories_sel", [])
    categories_sel = page.session.get("categories_sel")
    page.client_storage.set_async("loc_visited", [])
    page.client_storage.set_async("radius_sel", 1000)
    loc_visited = page.client_storage.get_async("loc_visited") 
    page.client_storage.set_async("sort_sel", "RELEVANCE")

    print(loc_visited)
    
    def view_pop(event): #Per anar enrere 
        #print("view pop:", event.view) #Això només imprimeix en terminal, de normal no cal
        if page.route == '/categories':
            page.views.pop()
            page.go('/')
        else: 
            page.views.pop()
            page.go("/configuracio")
       # top_view = page.views[-1]
        #  page.go(top_view.route)

    async def on_change_page(e):
        page.controls.clear() if page.route != '/info' else None
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
            page.add(configuracio)    
            images_saved.height = page.height
            images_saved.controls = []
            if len(loc_visited) > 0:
                page.views.append(View(controls=[AppBar(title=Text("Historial de Llocs"), adaptive=True,bgcolor="#AAD7D9"), images_saved],bgcolor = "#FFFCF1"))
                for i in range(len(loc_visited)):
                    images_saved.controls.append(
                        Container(content=Column(spacing=0.5,horizontal_alignment="center", controls=[Image(
                            src=f"https://picsum.photos/150/150?{i}",
                            border_radius=10), Text(f"{i}", text_align="center")
                    ])))
                    page.update()
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
            def radius(e):
                page.client_storage.set("radius_sel", round(e.control.value) * 1000)
                radius_sel = page.client_storage.get("radius_sel") 
                print(radius_sel)
            def sort(e):
                print(e.control.value)
                if e.control.value == "Valoració":
                    page.client_storage.set("sort_sel", "RATING")
                if e.control.value == "Rellevancia (default)":
                    page.client_storage.set("sort_sel", "RELEVANCE")
                if e.control.value == "Distància":
                    page.client_storage.set("sort_sel", "DISTANCE")
                if e.control.value == "Popularitat":
                    page.client_storage.set("sort_sel", "POPULARITY")
                sort_sel = page.client_storage.get("sort_sel") 
                print(sort_sel)
            radius_sel = page.client_storage.get("radius_sel")
            parametres_cerca = Column([
                Divider(),
                Text("RADI, DISTÀNCIA",weight=FontWeight.W_600, size=18),
                Text("Configura la distància màxima la qual vols que cerqui l'algorisme!",weight=FontWeight.W_300),
                Slider(min=1, max=10, divisions=10, label="{value} Km", value=radius_sel, on_change_end=radius,active_color="#7A9A9C", inactive_color="#c9d6d7"), #! No funciona el value per el async
                Divider(), 
                Text("RELLEVÀNCIA, ORDRE",weight=FontWeight.W_600, size=18),
                Text("Quins llocs t'apareixeran primer?",weight=FontWeight.W_300),
                Dropdown(
                        hint_text="Pica la teva preferencia",
                        width=page.width,
                        on_change=sort,
                        options=[
                            dropdown.Option("Rellevancia (default)"),
                            dropdown.Option("Valoració"),
                            dropdown.Option("Distància"),
                            dropdown.Option("Popularitat")]
                ),
                Divider(),
                Text("PREU",weight=FontWeight.W_600, size=18),
                Text("Configura el preu màxim que vols pagar de l'1 al 4! 1 (barat), 4 (car)",weight=FontWeight.W_300),
                Slider(min=0, max=4, divisions=4, label="{value}", on_change_end=print("hey"),active_color="#7A9A9C", inactive_color="#c9d6d7"),
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


    cards = []
    
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
        print(categories_sel)
    def categ_chip_sel(e):
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
        
        print(page.session.get("categories_sel"))
    
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
            
    def handle_swipe(e):
        asyncio.run(on_swipe(e))
    def handle_swipe_vertical(e):
        asyncio.run(on_swipe_vertical(e))
    
    # Aquest el que fa es convertir cada card individual en GestureDetector. Amb això, podem detectar cap a on es mou i com funciona. Es molt útil i ens ho serà en un futur.
    async def update_cards():
        stack_cards.controls.clear() 
        global index_photo_stack
        global images_request #! Variable local de sessió, també guardada dins de l'app
        #:) Solucionat tot emmagatzemat!!!!!!!!
        loc_visited = await page.client_storage.get_async("loc_visited") 
        categories_sel = page.session.get("categories_sel")
        sort_sel = await page.client_storage.get_async("sort_sel")
        radius_sel = await page.client_storage.get_async("radius_sel")
        loc_visited = await page.client_storage.get_async("loc_visited")
        print("sort_sel:", sort_sel)
        print("categories_sel:",categories_sel)
        print("radius_sel:",radius_sel)
        print("loc_visited:",loc_visited)
        if len(cards) == 0:
                index_photo_stack = -1
                #* Demanem les dades 
                #:) Cobren el mateix demanant 5, 10 que 50
 
                #llocs = Llocs(41.446081380886504,2.2491992381345103,radius_key,10,loc_visited_key,categories_key,sort_key) #! Problema, dona sempre el mateix BUG-5
                #dadesLlocs, loc_visited = llocs.dades()
                #print(dadesLlocs)
                dadesLlocs = [{'fsq_id': '54c94eab498e13f929e140ca', 'categories': [{'id': 13026, 'name': 'BBQ Joint', 'short_name': 'BBQ', 'plural_name': 'BBQ Joints', 'icon': {'prefix': 'https://ss3.4sqi.net/img/categories_v2/food/bbqalt_', 'suffix': '.png'}}, {'id': 13031, 'name': 'Burger Joint', 'short_name': 'Burgers', 'plural_name': 'Burger Joints', 'icon': {'prefix': 'https://ss3.4sqi.net/img/categories_v2/food/burger_', 'suffix': '.png'}}, {'id': 13145, 'name': 'Fast Food Restaurant', 'short_name': 'Fast Food', 'plural_name': 'Fast Food Restaurants', 'icon': {'prefix': 'https://ss3.4sqi.net/img/categories_v2/food/fastfood_', 'suffix': '.png'}}], 'chains': [], 'closed_bucket': 'VeryLikelyOpen', 'distance': 145, 'geocodes': {'drop_off': {'latitude': 41.447179, 'longitude': 2.250109}, 'main': {'latitude': 41.447213, 'longitude': 2.250087}, 'roof': {'latitude': 41.447213, 'longitude': 2.250087}}, 'location': {'address': 'Sant Carles, 2', 'admin_region': 'Cataluña', 'country': 'ES', 'cross_street': 'carrer del mar', 'formatted_address': 'Sant Carles, 2 (carrer del mar), 08911 Badalona Catalunya', 'locality': 'Badalona', 'postcode': '08911', 'region': 'Catalunya'}, 'name': "Charlotte's Grill", 'photos': [{'id': '5dbc72be430f5b00075afd5a', 'created_at': '2019-11-01T18:00:30.000Z', 'prefix': 'https://fastly.4sqi.net/img/general/', 'suffix': '/493471249_pTAxRvc8szOjFqap5D7LrnSYNn6WUSxCY6pzx_qfpbE.jpg', 'width': 1440, 'height': 1920}, {'id': '5adc9d65ee628b274a17580e', 'created_at': '2018-04-22T14:34:13.000Z', 'prefix': 'https://fastly.4sqi.net/img/general/', 'suffix': '/89119159_5_8O_XqPTLXFhp0kugnndSvUZrM1X5rMUUYvajFszEE.jpg', 'width': 1920, 'height': 1440, 'classifications': ['food']}, {'id': '588e13e4109dfe38b2e8c949', 'created_at': '2017-01-29T16:10:12.000Z', 'prefix': 'https://fastly.4sqi.net/img/general/', 'suffix': '/4304162_aDs3B5FzjUqyfDt41yvHQwgcmXlkPvV1NzElz1iuKu4.jpg', 'width': 1920, 'height': 1440, 'classifications': ['food']}, {'id': '575743f8498e571fdc8af90d', 'created_at': '2016-06-07T22:00:24.000Z', 'prefix': 'https://fastly.4sqi.net/img/general/', 'suffix': '/38193938_jp9yyycsDZGDfBVE6K3eVC57rTy_8r0ZYyYfy42bQhA.jpg', 'width': 5312, 'height': 2988}, {'id': '574af40acd10c9410e617835', 'created_at': '2016-05-29T13:52:10.000Z', 'prefix': 'https://fastly.4sqi.net/img/general/', 'suffix': '/67818144_IYuPS_nK-sDXmViN3ijb5DR-7sPtDfOR7ZNU-NFHHKg.jpg', 'width': 1440, 'height': 1920, 'classifications': ['food']}], 'price': 2, 'rating': 8.7, 'related_places': {}, 'social_media': {'twitter': 'charlottesgrill'}, 'timezone': 'Europe/Madrid'}, {'fsq_id': '4c08034a340720a15f768293', 'categories': [{'id': 13302, 'name': 'Mediterranean Restaurant', 'short_name': 'Mediterranean', 'plural_name': 'Mediterranean Restaurants', 'icon': {'prefix': 'https://ss3.4sqi.net/img/categories_v2/food/mediterranean_', 'suffix': '.png'}}], 'chains': [], 'closed_bucket': 'LikelyOpen', 'distance': 140, 'geocodes': {'drop_off': {'latitude': 41.447187, 'longitude': 2.248304}, 'main': {'latitude': 41.447157, 'longitude': 2.248323}, 'roof': {'latitude': 41.447157, 'longitude': 2.248323}}, 'location': {'address': 'Carrer del Lleó, 98', 'admin_region': 'Cataluña', 'country': 'ES', 'formatted_address': 'Carrer del Lleó, 98, 08911 Badalona Catalunya', 'locality': 'Badalona', 'postcode': '08911', 'region': 'Catalunya'}, 'name': "Ca l'Arqué", 'photos': [{'id': '5b24fb3cda7080002c51f79c', 'created_at': '2018-06-16T11:57:48.000Z', 'prefix': 'https://fastly.4sqi.net/img/general/', 'suffix': '/209508005_xmMcJH4864s7dccOvwmqexKLSM5pRz-54a_-ZY28VQQ.jpg', 'width': 1440, 'height': 1920, 'classifications': ['food']}, {'id': '58c31841260327384a2b39a0', 'created_at': '2017-03-10T21:18:57.000Z', 'prefix': 'https://fastly.4sqi.net/img/general/', 'suffix': '/91959299__rqd9q4Ar2-Q8TrDpkfKCExTpeZ4wIDSbEAEE1yClAQ.jpg', 'width': 1080, 'height': 1920}, {'id': '578643c6498e696c6a19a717', 'created_at': '2016-07-13T13:36:06.000Z', 'prefix': 'https://fastly.4sqi.net/img/general/', 'suffix': '/209508005_v2rMIo6kmvFigjay1HormcqDfAghtoSwuCxUukLtUes.jpg', 'width': 1440, 'height': 1920, 'classifications': ['food']}, {'id': '55391ae5498eb5a03be8bdf7', 'created_at': '2015-04-23T16:16:37.000Z', 'prefix': 'https://fastly.4sqi.net/img/general/', 'suffix': '/10297454_cyhW8iSdKm7yRqdrJUwx5RZpKNqtgq94mARZMSvn5Lg.jpg', 'width': 1440, 'height': 1920, 'classifications': ['food']}, {'id': '54a92e0c498ecad0d89fb085', 'created_at': '2015-01-04T12:11:56.000Z', 'prefix': 'https://fastly.4sqi.net/img/general/', 'suffix': '/30733862_WcjHYi9xUv-_mcWKHcNNUtH1kQ5AcRDIH7Y05S_OhnI.jpg', 'width': 1440, 'height': 1920, 'classifications': ['food']}], 'price': 2, 'rating': 7.8, 'related_places': {}, 'social_media': {}, 'timezone': 'Europe/Madrid'}, {'fsq_id': '4be197b1fc2376b080c469a9', 'categories': [{'id': 13035, 'name': 'Coffee Shop', 'short_name': 'Coffee Shop', 'plural_name': 'Coffee Shops', 'icon': {'prefix': 'https://ss3.4sqi.net/img/categories_v2/food/coffeeshop_', 'suffix': '.png'}}, {'id': 13046, 'name': 'Ice Cream Parlor', 'short_name': 'Ice Cream', 'plural_name': 'Ice Cream Parlors', 'icon': {'prefix': 'https://ss3.4sqi.net/img/categories_v2/food/icecream_', 'suffix': '.png'}}, {'id': 13065, 'name': 'Restaurant', 'short_name': 'Restaurant', 'plural_name': 'Restaurants', 'icon': {'prefix': 'https://ss3.4sqi.net/img/categories_v2/food/default_', 'suffix': '.png'}}], 'chains': [], 'closed_bucket': 'VeryLikelyOpen', 'distance': 216, 'geocodes': {'main': {'latitude': 41.448019, 'longitude': 2.249516}, 'roof': {'latitude': 41.448019, 'longitude': 2.249516}}, 'location': {'address': 'Carrer Mar, 97', 'address_extended': 'Bajo', 'admin_region': 'Cataluña', 'country': 'ES', 'cross_street': 'Ribes i Perdigó', 'formatted_address': 'Carrer Mar, 97 (Ribes i Perdigó), 08911 Badalona Catalunya', 'locality': 'Badalona', 'postcode': '08911', 'region': 'Catalunya'}, 'name': 'Can Soler', 'photos': [{'id': '6506f93e77ab7a7492e7d019', 'created_at': '2023-09-17T13:03:58.000Z', 'prefix': 'https://fastly.4sqi.net/img/general/', 'suffix': '/1155361_-97JsI0c31PcZvsN0xSPzpTpa1olyfg8HgejN5Qc9kA.jpg', 'width': 1440, 'height': 1440}, {'id': '5f32d0556419c108d24d4697', 'created_at': '2020-08-11T17:07:33.000Z', 'prefix': 'https://fastly.4sqi.net/img/general/', 'suffix': '/63332301_OPSQur0wEPIInNCGA5i_6O9wxlJMkye6eNe9yu_3g_E.jpg', 'width': 1080, 'height': 1440}, {'id': '592eb9882bf9a9463e5d7879', 'created_at': '2017-05-31T12:39:36.000Z', 'prefix': 'https://fastly.4sqi.net/img/general/', 'suffix': '/63317963_YkZxzfAODCt0Omem-bebdXodQRXZtelyRVttYnORt00.jpg', 'width': 1920, 'height': 1440, 'classifications': ['food']}, {'id': '590ef58c61f0701b46b31883', 'created_at': '2017-05-07T10:23:08.000Z', 'prefix': 'https://fastly.4sqi.net/img/general/', 'suffix': '/79698049__J7fW0S327ZmgJBW8kJFzjxwnkTsR-7-n70M2cCxEmM.jpg', 'width': 1920, 'height': 1440}, {'id': '58cece774bc2f1351e1cd41a', 'created_at': '2017-03-19T18:31:19.000Z', 'prefix': 'https://fastly.4sqi.net/img/general/', 'suffix': '/79698049_Yf7vPQi1eWtB-b_NsQtgamd9JvbVBro5gsdtOIb4dME.jpg', 'width': 1440, 'height': 1920}], 'price': 2, 'rating': 8.5, 'related_places': {}, 'social_media': {}, 'timezone': 'Europe/Madrid'}, {'fsq_id': '4b8eced4f964a520653833e3', 'categories': [{'id': 13064, 'name': 'Pizzeria', 'short_name': 'Pizza', 'plural_name': 'Pizzerias', 'icon': {'prefix': 'https://ss3.4sqi.net/img/categories_v2/food/pizza_', 'suffix': '.png'}}, {'id': 13145, 'name': 'Fast Food Restaurant', 'short_name': 'Fast Food', 'plural_name': 'Fast Food Restaurants', 'icon': {'prefix': 'https://ss3.4sqi.net/img/categories_v2/food/fastfood_', 'suffix': '.png'}}, {'id': 13334, 'name': 'Sandwich Spot', 'short_name': 'Sandwich Spot', 'plural_name': 'Sandwich Spots', 'icon': {'prefix': 'https://ss3.4sqi.net/img/categories_v2/food/deli_', 'suffix': '.png'}}], 'chains': [], 'closed_bucket': 'VeryLikelyOpen', 'distance': 204, 'geocodes': {'main': {'latitude': 41.447853, 'longitude': 2.249885}, 'roof': {'latitude': 41.447853, 'longitude': 2.249885}}, 'location': {'address': 'Carrer del Tei, 7', 'admin_region': 'Cataluña', 'country': 'ES', 'cross_street': 'carrer del mar', 'formatted_address': 'Carrer del Tei, 7 (carrer del mar), 08911 Badalona Catalunya', 'locality': 'Badalona', 'postcode': '08911', 'region': 'Catalunya'}, 'name': 'Neruca', 'photos': [{'id': '5d486f8b3a3c700007234669', 'created_at': '2019-08-05T18:03:55.000Z', 'prefix': 'https://fastly.4sqi.net/img/general/', 'suffix': '/10297454_P7H9DLKojEyyA6FwEarbih8hUDk1iYCrZpPV-XXAngE.jpg', 'width': 1440, 'height': 1920, 'classifications': ['food']}, {'id': '57c095b2498e56195483c39c', 'created_at': '2016-08-26T19:17:06.000Z', 'prefix': 'https://fastly.4sqi.net/img/general/', 'suffix': '/72324205_BBP16AvGCkkPEa-BvcRAdDPP4ZkbvDRAUTvEMOWAvZA.jpg', 'width': 2988, 'height': 5312}, {'id': '57a635dc498ea46a29c1dc65', 'created_at': '2016-08-06T19:09:16.000Z', 'prefix': 'https://fastly.4sqi.net/img/general/', 'suffix': '/72324205_DcDNsjmSLQ3-ZUlLl9cuRQJKy43bapzpQjgT3LskzkU.jpg', 'width': 5312, 'height': 2988}, {'id': '55469bd8498ef8a7ee0fa059', 'created_at': '2015-05-03T22:06:16.000Z', 'prefix': 'https://fastly.4sqi.net/img/general/', 'suffix': '/26910369_gblcczWZkoG6NO4rAUMMFWZsCA7V6wTR3VXJtpCFx_U.jpg', 'width': 1432, 'height': 1920, 'classifications': ['food']}], 'price': 1, 'rating': 8.1, 'related_places': {}, 'social_media': {'facebook_id': '51843469090'}, 'timezone': 'Europe/Madrid'}, {'fsq_id': '535292d9498ef40efbc96c55', 'categories': [{'id': 13288, 'name': 'Kebab Restaurant', 'short_name': 'Kebab', 'plural_name': 'Kebab Restaurants', 'icon': {'prefix': 'https://ss3.4sqi.net/img/categories_v2/food/middleeastern_', 'suffix': '.png'}}, {'id': 13356, 'name': 'Turkish Restaurant', 'short_name': 'Turkish', 'plural_name': 'Turkish Restaurants', 'icon': {'prefix': 'https://ss3.4sqi.net/img/categories_v2/food/turkish_', 'suffix': '.png'}}], 'chains': [], 'closed_bucket': 'VeryLikelyOpen', 'distance': 212, 'geocodes': {'main': {'latitude': 41.447971, 'longitude': 2.249567}, 'roof': {'latitude': 41.447971, 'longitude': 2.249567}}, 'location': {'address': 'Carrer del Mar, 106', 'admin_region': 'Cataluña', 'country': 'ES', 'cross_street': '', 'formatted_address': 'Carrer del Mar, 106, 08911 Badalona Catalunya', 'locality': 'Badalona', 'postcode': '08911', 'region': 'Catalunya'}, 'name': 'Bella Istanbul', 'photos': [{'id': '6290e77daf913f62b206bf89', 'created_at': '2022-05-27T15:00:13.000Z', 'prefix': 'https://fastly.4sqi.net/img/general/', 'suffix': '/11012402_OOtLuREQ5psxuxT1XZF8NEpqLfKyOuhIBixABXlMiX8.jpg', 'width': 1920, 'height': 1440}, {'id': '6290e4b28d6fb3643aba2307', 'created_at': '2022-05-27T14:48:18.000Z', 'prefix': 'https://fastly.4sqi.net/img/general/', 'suffix': '/11012402_jFOLsDCj2E7AFh30KeUV35OvOkiFH6yFC8locE9K9t0.jpg', 'width': 1920, 'height': 1440}, {'id': '6290e4afa6b3ec3807ee7958', 'created_at': '2022-05-27T14:48:15.000Z', 'prefix': 'https://fastly.4sqi.net/img/general/', 'suffix': '/11012402_qvvIeZJ9gdrBmxd6jqUbgJODwiwGY_b72PVd0TPd0mE.jpg', 'width': 1920, 'height': 1440}, {'id': '59207bd1112c6c4c4cf6c5e1', 'created_at': '2017-05-20T17:24:33.000Z', 'prefix': 'https://fastly.4sqi.net/img/general/', 'suffix': '/3498714_wGI4uZC8Z7BZA5zvCNXsZzsZcigOOIrmXSelSrIKHzs.jpg', 'width': 1440, 'height': 1920}, {'id': '580b9dda38fa8903751c7696', 'created_at': '2016-10-22T17:11:54.000Z', 'prefix': 'https://fastly.4sqi.net/img/general/', 'suffix': '/48025561_LciG6NtJXoZga3JsCez2wl3Z-NvvpGS0A9XNojpivMk.jpg', 'width': 1919, 'height': 1121, 'classifications': ['food']}], 'price': 1, 'rating': 8.0, 'related_places': {}, 'social_media': {'twitter': 'bella_istanbul'}, 'timezone': 'Europe/Madrid'}, {'fsq_id': '4c591415b05c1b8d1101d5b1', 'categories': [{'id': 16003, 'name': 'Beach', 'short_name': 'Beach', 'plural_name': 'Beaches', 'icon': {'prefix': 'https://ss3.4sqi.net/img/categories_v2/parks_outdoors/beach_', 'suffix': '.png'}}], 'chains': [], 'closed_bucket': 'VeryLikelyOpen', 'distance': 307, 'geocodes': {'main': {'latitude': 41.44827, 'longitude': 2.251455}, 'roof': {'latitude': 41.44827, 'longitude': 2.251455}}, 'location': {'admin_region': 'Cataluña', 'country': 'ES', 'cross_street': '', 'formatted_address': '08912 Badalona Catalunya', 'locality': 'Badalona', 'postcode': '08912', 'region': 'Catalunya'}, 'name': 'Platja dels Pescadors', 'photos': [{'id': '6506d1c656a2eb0f86e8424c', 'created_at': '2023-09-17T10:15:34.000Z', 'prefix': 'https://fastly.4sqi.net/img/general/', 'suffix': '/1155361_CMghvt2Z0se0A1cplhofBX75fVb9f7QAXmr0Dndt-1c.jpg', 'width': 1920, 'height': 1440}, {'id': '6506d1c577ab7a74924609d8', 'created_at': '2023-09-17T10:15:33.000Z', 'prefix': 'https://fastly.4sqi.net/img/general/', 'suffix': '/1155361_YoSYNbWD0jWfN3kBTpCI6PUnSt3mXVYzmrn6DDramIQ.jpg', 'width': 1920, 'height': 1440}, {'id': '640f55bb3fefa11dc6e574e9', 'created_at': '2023-03-13T16:56:27.000Z', 'prefix': 'https://fastly.4sqi.net/img/general/', 'suffix': '/54053478_ujB1-DAIq6iQ694cJAMVxqxL3VKw3QP3czH9o8TAGjg.jpg', 'width': 1440, 'height': 1920}, {'id': '62bdd508d922f43fe9a9e4b5', 'created_at': '2022-06-30T16:53:28.000Z', 'prefix': 'https://fastly.4sqi.net/img/general/', 'suffix': '/20522136_mYP0kKgJgRr4YO_7eS9gTleeMyFugt_IOjRnXjarRHQ.jpg', 'width': 1920, 'height': 1440}, {'id': '6069ca322ec75a04d0d1ba97', 'created_at': '2021-04-04T14:16:18.000Z', 'prefix': 'https://fastly.4sqi.net/img/general/', 'suffix': '/12767036_ixCc2llOklbMy7hdtq2O3ukhXbCKF1JNIQVUSU9AhFc.jpg', 'width': 1440, 'height': 1920}], 'rating': 8.7, 'related_places': {}, 'social_media': {}, 'timezone': 'Europe/Madrid'}, {'fsq_id': '4bbf72f8ba9776b05b26ffc8', 'categories': [{'id': 13003, 'name': 'Bar', 'short_name': 'Bar', 'plural_name': 'Bars', 'icon': {'prefix': 'https://ss3.4sqi.net/img/categories_v2/nightlife/pub_', 'suffix': '.png'}}], 'chains': [], 'closed_bucket': 'LikelyOpen', 'distance': 355, 'geocodes': {'drop_off': {'latitude': 41.449225, 'longitude': 2.249659}, 'main': {'latitude': 41.449268, 'longitude': 2.249624}, 'roof': {'latitude': 41.449268, 'longitude': 2.249624}}, 'location': {'address': 'Calle Baranera, 39', 'admin_region': 'Cataluña', 'country': 'ES', 'formatted_address': 'Calle Baranera, 39, 08911 Badalona Catalunya', 'locality': 'Badalona', 'postcode': '08911', 'region': 'Catalunya'}, 'name': 'Torras Garriga, J', 'photos': [{'id': '65b41508bdcb696b1f4a8a0e', 'created_at': '2024-01-26T20:24:40.000Z', 'prefix': 'https://fastly.4sqi.net/img/general/', 'suffix': '/23910712_1_duUH8czk_5ktvoIDFVSgcCcPIwc9g1kYGtsn-YZ_4.jpg', 'width': 1920, 'height': 1440}, {'id': '65b41091b70ea41594c4eb09', 'created_at': '2024-01-26T20:05:37.000Z', 'prefix': 'https://fastly.4sqi.net/img/general/', 'suffix': '/23910712_Un2WyBHEKW967_HQ3IBrQDVTGLjJ4UItn4AiTT1f6bA.jpg', 'width': 1920, 'height': 1440}, {'id': '64fcceb7c381f46e81493a39', 'created_at': '2023-09-09T19:59:51.000Z', 'prefix': 'https://fastly.4sqi.net/img/general/', 'suffix': '/23910712_6jeQ-I23iztTYeFBkAhiue_k3E5gfawJzbNLzuxAbm8.jpg', 'width': 1440, 'height': 1920}, {'id': '571e59a0498e4010ddda55f7', 'created_at': '2016-04-25T17:53:36.000Z', 'prefix': 'https://fastly.4sqi.net/img/general/', 'suffix': '/79041888_t3HpbQG7SB_zJH3VaEnzPmSnMcYm6EZFjkt11UDokCE.jpg', 'width': 1440, 'height': 1920, 'classifications': ['indoor']}], 'price': 2, 'rating': 8.4, 'related_places': {}, 'social_media': {}, 'timezone': 'Europe/Madrid'}, {'fsq_id': '4b50b20bf964a520ef2d27e3', 'categories': [{'id': 13006, 'name': 'Beer Bar', 'short_name': 'Beer Bar', 'plural_name': 'Beer Bars', 'icon': {'prefix': 'https://ss3.4sqi.net/img/categories_v2/nightlife/pub_', 'suffix': '.png'}}, {'id': 13065, 'name': 'Restaurant', 'short_name': 'Restaurant', 'plural_name': 'Restaurants', 'icon': {'prefix': 'https://ss3.4sqi.net/img/categories_v2/food/default_', 'suffix': '.png'}}], 'chains': [], 'closed_bucket': 'VeryLikelyOpen', 'distance': 361, 'geocodes': {'main': {'latitude': 41.449012, 'longitude': 2.247306}, 'roof': {'latitude': 41.449012, 'longitude': 2.247306}}, 'location': {'address': 'Lleó, 33', 'admin_region': 'Cataluña', 'country': 'ES', 'cross_street': '', 'formatted_address': 'Lleó, 33, 08911 Badalona Catalunya', 'locality': 'Badalona', 'postcode': '08911', 'region': 'Catalunya'}, 'name': '4 Pedres', 'photos': [{'id': '62f4007b746a243383848fe4', 'created_at': '2022-08-10T19:01:15.000Z', 'prefix': 'https://fastly.4sqi.net/img/general/', 'suffix': '/8567928_3zgRBNoZNT1Cjclupr-nUkDtEblI9GTHGKL1CEC2z1Q.jpg', 'width': 1816, 'height': 2993}, {'id': '6211417bd6fddc3eff9635ff', 'created_at': '2022-02-19T19:14:03.000Z', 'prefix': 'https://fastly.4sqi.net/img/general/', 'suffix': '/8567928_PNfxVhBJ836oGXyEIlPqbsLeo1X7u4LfLJI2aCPZH9U.jpg', 'width': 1816, 'height': 2945}, {'id': '61ca08bed417b73516659f8f', 'created_at': '2021-12-27T18:41:02.000Z', 'prefix': 'https://fastly.4sqi.net/img/general/', 'suffix': '/8567928_NW64pN-n2msJ07VK4jOjtnwed4-BY_M5u-vPjLLrYZs.jpg', 'width': 1088, 'height': 2304}, {'id': '6102dcbcb3566219555f49a2', 'created_at': '2021-07-29T16:52:12.000Z', 'prefix': 'https://fastly.4sqi.net/img/general/', 'suffix': '/8567928_dmaOyUPsGE4Few1bYbd1Otk2ipDLPnx0qWQ-mXApsF0.jpg', 'width': 1728, 'height': 2304}, {'id': '5cba01612b98440039c89b5f', 'created_at': '2019-04-19T17:12:01.000Z', 'prefix': 'https://fastly.4sqi.net/img/general/', 'suffix': '/8567928_qoMXxwQGZjM09AKh-hJZ8xABPLinA2Lfyb6RKGACA-c.jpg', 'width': 1500, 'height': 2000, 'classifications': ['food']}], 'rating': 8.5, 'related_places': {}, 'social_media': {}, 'timezone': 'Europe/Madrid'}, {'fsq_id': '4c0932b5340720a103588493', 'categories': [{'id': 13002, 'name': 'Bakery', 'short_name': 'Bakery', 'plural_name': 'Bakeries', 'icon': {'prefix': 'https://ss3.4sqi.net/img/categories_v2/food/bakery_', 'suffix': '.png'}}], 'chains': [], 'closed_bucket': 'VeryLikelyOpen', 'distance': 419, 'geocodes': {'main': {'latitude': 41.449696, 'longitude': 2.247729}, 'roof': {'latitude': 41.449696, 'longitude': 2.247729}}, 'location': {'address': 'Calle Mar, 5', 'admin_region': 'Cataluña', 'country': 'ES', 'cross_street': '', 'formatted_address': 'Calle Mar, 5, 08911 Badalona Catalunya', 'locality': 'Badalona', 'postcode': '08911', 'region': 'Catalunya'}, 'name': 'Forn Bertran', 'photos': [{'id': '5e5b8c5d36734600089a913e', 'created_at': '2020-03-01T10:20:13.000Z', 'prefix': 'https://fastly.4sqi.net/img/general/', 'suffix': '/67909_g6Ik7Afc5DLtftGtyGeMNTyMYxkF7fkrKchUAlk9yRk.jpg', 'width': 1440, 'height': 1920}, {'id': '5aed66db0457b7002c7437f5', 'created_at': '2018-05-05T08:10:03.000Z', 'prefix': 'https://fastly.4sqi.net/img/general/', 'suffix': '/88652692_MZYjBb89PNxB6SU8y3G7MYGVnvJ3uJq3W8a8Q8HZCRY.jpg', 'width': 1440, 'height': 1920}, {'id': '5ae46a77c9a517002cff194d', 'created_at': '2018-04-28T12:35:03.000Z', 'prefix': 'https://fastly.4sqi.net/img/general/', 'suffix': '/328094992_yb2PZiF7EONf_1e-mf5MjtHPYW-pONtziks1chvG9Zs.jpg', 'width': 1440, 'height': 1920, 'classifications': ['food']}, {'id': '5ad6079f4a7aae2942815ecb', 'created_at': '2018-04-17T14:41:35.000Z', 'prefix': 'https://fastly.4sqi.net/img/general/', 'suffix': '/89376305_XW011nNjuEDdyOSXoTIAJPkHVj24t-ozeF4t04Olokw.jpg', 'width': 1920, 'height': 1440, 'classifications': ['outdoor']}, {'id': '5a6daa36d552c712a6d5252b', 'created_at': '2018-01-28T10:47:18.000Z', 'prefix': 'https://fastly.4sqi.net/img/general/', 'suffix': '/2462338_W7zBsoS2s8tBiiIdTBwUSiliuBUYGwgrCDNslliqMTo.jpg', 'width': 1920, 'height': 1440, 'classifications': ['food']}], 'price': 2, 'rating': 8.3, 'related_places': {}, 'social_media': {'facebook_id': '130926050273606', 'twitter': 'fornbertranmar'}, 'timezone': 'Europe/Madrid'}, {'fsq_id': '4b76ead5f964a5205b6a2ee3', 'categories': [{'id': 13334, 'name': 'Sandwich Spot', 'short_name': 'Sandwich Spot', 'plural_name': 'Sandwich Spots', 'icon': {'prefix': 'https://ss3.4sqi.net/img/categories_v2/food/deli_', 'suffix': '.png'}}], 'chains': [], 'closed_bucket': 'LikelyOpen', 'distance': 432, 'geocodes': {'drop_off': {'latitude': 41.44974, 'longitude': 2.247579}, 'main': {'latitude': 41.449792, 'longitude': 2.247627}, 'roof': {'latitude': 41.449792, 'longitude': 2.247627}}, 'location': {'address': 'Calle del Mar, 1', 'admin_region': 'Cataluña', 'country': 'ES', 'cross_street': 'Plaça de la Vila', 'formatted_address': 'Calle del Mar, 1 (Plaça de la Vila), 08915 Badalona Catalunya', 'locality': 'Badalona', 'postcode': '08915', 'region': 'Catalunya'}, 'name': "Frankfurt's Vallès", 'photos': [{'id': '5c7c2083b9a5a8002c3e7e90', 'created_at': '2019-03-03T18:44:19.000Z', 'prefix': 'https://fastly.4sqi.net/img/general/', 'suffix': '/11191832_VTp_tkBb6sDP6jGuqQiGLkm_cBS_SIb7UIxFSG7xoa4.jpg', 'width': 4032, 'height': 3024}, {'id': '5c7c122e66fc650039cdc307', 'created_at': '2019-03-03T17:43:10.000Z', 'prefix': 'https://fastly.4sqi.net/img/general/', 'suffix': '/11191832_FFseIiQA_zXJEA9BmWLeg2id_hBFMO-es21LcjGBQJo.jpg', 'width': 1500, 'height': 2000, 'classifications': ['food']}, {'id': '5af08dae81635b002c1963db', 'created_at': '2018-05-07T17:32:30.000Z', 'prefix': 'https://fastly.4sqi.net/img/general/', 'suffix': '/5116689_AYUVMJUjvmB5FcSO-XTqmgQ3sPADB6Igft7Ep4JChLU.jpg', 'width': 1440, 'height': 1920}, {'id': '58d039b3af5c143843cce5f0', 'created_at': '2017-03-20T20:21:07.000Z', 'prefix': 'https://fastly.4sqi.net/img/general/', 'suffix': '/1817856_ZNVmoO83rDyIQoKLi_4jtJayprPxkHC3v7L8mM4fP7Y.jpg', 'width': 1440, 'height': 1920}, {'id': '51252d71e4b03bd2d4ac979f', 'created_at': '2013-02-20T20:09:21.000Z', 'prefix': 'https://fastly.4sqi.net/img/general/', 'suffix': '/7835341_cNL6lUvIs2cfe9S5Q6H_M7KFnIryE7r4ZD08Ny_yqxM.jpg', 'width': 960, 'height': 720}], 'price': 1, 'rating': 8.1, 'related_places': {}, 'social_media': {}, 'timezone': 'Europe/Madrid'}]
                # print(dadesLlocs)
                if dadesLlocs == []:
                    print("Això no ha de passar!") 
                #images_request = llocs.photos()
                images_request = [['https://fastly.4sqi.net/img/general/1440x1920/209508005_xmMcJH4864s7dccOvwmqexKLSM5pRz-54a_-ZY28VQQ.jpg'], [], ['https://fastly.4sqi.net/img/general/1440x1440/1155361_-97JsI0c31PcZvsN0xSPzpTpa1olyfg8HgejN5Qc9kA.jpg', 'https://fastly.4sqi.net/img/general/1080x1440/63332301_OPSQur0wEPIInNCGA5i_6O9wxlJMkye6eNe9yu_3g_E.jpg', 'https://fastly.4sqi.net/img/general/1920x1440/63317963_YkZxzfAODCt0Omem-bebdXodQRXZtelyRVttYnORt00.jpg', 'https://fastly.4sqi.net/img/general/1920x1440/79698049__J7fW0S327ZmgJBW8kJFzjxwnkTsR-7-n70M2cCxEmM.jpg', 'https://fastly.4sqi.net/img/general/1440x1920/79698049_Yf7vPQi1eWtB-b_NsQtgamd9JvbVBro5gsdtOIb4dME.jpg'], ['https://fastly.4sqi.net/img/general/1440x1920/10297454_P7H9DLKojEyyA6FwEarbih8hUDk1iYCrZpPV-XXAngE.jpg', 'https://fastly.4sqi.net/img/general/2988x5312/72324205_BBP16AvGCkkPEa-BvcRAdDPP4ZkbvDRAUTvEMOWAvZA.jpg', 'https://fastly.4sqi.net/img/general/5312x2988/72324205_DcDNsjmSLQ3-ZUlLl9cuRQJKy43bapzpQjgT3LskzkU.jpg', 'https://fastly.4sqi.net/img/general/1432x1920/26910369_gblcczWZkoG6NO4rAUMMFWZsCA7V6wTR3VXJtpCFx_U.jpg'], ['https://fastly.4sqi.net/img/general/1920x1440/11012402_OOtLuREQ5psxuxT1XZF8NEpqLfKyOuhIBixABXlMiX8.jpg', 'https://fastly.4sqi.net/img/general/1920x1440/11012402_jFOLsDCj2E7AFh30KeUV35OvOkiFH6yFC8locE9K9t0.jpg', 'https://fastly.4sqi.net/img/general/1920x1440/11012402_qvvIeZJ9gdrBmxd6jqUbgJODwiwGY_b72PVd0TPd0mE.jpg', 'https://fastly.4sqi.net/img/general/1440x1920/3498714_wGI4uZC8Z7BZA5zvCNXsZzsZcigOOIrmXSelSrIKHzs.jpg', 'https://fastly.4sqi.net/img/general/1919x1121/48025561_LciG6NtJXoZga3JsCez2wl3Z-NvvpGS0A9XNojpivMk.jpg'], ['https://fastly.4sqi.net/img/general/1920x1440/1155361_CMghvt2Z0se0A1cplhofBX75fVb9f7QAXmr0Dndt-1c.jpg', 'https://fastly.4sqi.net/img/general/1920x1440/1155361_YoSYNbWD0jWfN3kBTpCI6PUnSt3mXVYzmrn6DDramIQ.jpg', 'https://fastly.4sqi.net/img/general/1440x1920/54053478_ujB1-DAIq6iQ694cJAMVxqxL3VKw3QP3czH9o8TAGjg.jpg', 'https://fastly.4sqi.net/img/general/1920x1440/20522136_mYP0kKgJgRr4YO_7eS9gTleeMyFugt_IOjRnXjarRHQ.jpg', 'https://fastly.4sqi.net/img/general/1440x1920/12767036_ixCc2llOklbMy7hdtq2O3ukhXbCKF1JNIQVUSU9AhFc.jpg'], ['https://fastly.4sqi.net/img/general/1920x1440/23910712_1_duUH8czk_5ktvoIDFVSgcCcPIwc9g1kYGtsn-YZ_4.jpg', 'https://fastly.4sqi.net/img/general/1920x1440/23910712_Un2WyBHEKW967_HQ3IBrQDVTGLjJ4UItn4AiTT1f6bA.jpg', 'https://fastly.4sqi.net/img/general/1440x1920/23910712_6jeQ-I23iztTYeFBkAhiue_k3E5gfawJzbNLzuxAbm8.jpg', 'https://fastly.4sqi.net/img/general/1440x1920/79041888_t3HpbQG7SB_zJH3VaEnzPmSnMcYm6EZFjkt11UDokCE.jpg'], ['https://fastly.4sqi.net/img/general/1816x2993/8567928_3zgRBNoZNT1Cjclupr-nUkDtEblI9GTHGKL1CEC2z1Q.jpg', 'https://fastly.4sqi.net/img/general/1816x2945/8567928_PNfxVhBJ836oGXyEIlPqbsLeo1X7u4LfLJI2aCPZH9U.jpg', 'https://fastly.4sqi.net/img/general/1088x2304/8567928_NW64pN-n2msJ07VK4jOjtnwed4-BY_M5u-vPjLLrYZs.jpg', 'https://fastly.4sqi.net/img/general/1728x2304/8567928_dmaOyUPsGE4Few1bYbd1Otk2ipDLPnx0qWQ-mXApsF0.jpg', 'https://fastly.4sqi.net/img/general/1500x2000/8567928_qoMXxwQGZjM09AKh-hJZ8xABPLinA2Lfyb6RKGACA-c.jpg'], ['https://fastly.4sqi.net/img/general/1440x1920/67909_g6Ik7Afc5DLtftGtyGeMNTyMYxkF7fkrKchUAlk9yRk.jpg', 'https://fastly.4sqi.net/img/general/1440x1920/88652692_MZYjBb89PNxB6SU8y3G7MYGVnvJ3uJq3W8a8Q8HZCRY.jpg', 'https://fastly.4sqi.net/img/general/1440x1920/328094992_yb2PZiF7EONf_1e-mf5MjtHPYW-pONtziks1chvG9Zs.jpg', 'https://fastly.4sqi.net/img/general/1920x1440/89376305_XW011nNjuEDdyOSXoTIAJPkHVj24t-ozeF4t04Olokw.jpg', 'https://fastly.4sqi.net/img/general/1920x1440/2462338_W7zBsoS2s8tBiiIdTBwUSiliuBUYGwgrCDNslliqMTo.jpg'], ['https://fastly.4sqi.net/img/general/4032x3024/11191832_VTp_tkBb6sDP6jGuqQiGLkm_cBS_SIb7UIxFSG7xoa4.jpg', 'https://fastly.4sqi.net/img/general/1500x2000/11191832_FFseIiQA_zXJEA9BmWLeg2id_hBFMO-es21LcjGBQJo.jpg', 'https://fastly.4sqi.net/img/general/1440x1920/5116689_AYUVMJUjvmB5FcSO-XTqmgQ3sPADB6Igft7Ep4JChLU.jpg', 'https://fastly.4sqi.net/img/general/1440x1920/1817856_ZNVmoO83rDyIQoKLi_4jtJayprPxkHC3v7L8mM4fP7Y.jpg', 'https://fastly.4sqi.net/img/general/960x720/7835341_cNL6lUvIs2cfe9S5Q6H_M7KFnIryE7r4ZD08Ny_yqxM.jpg']]
                # print(images_request)
                #categories = llocs.categories()
                categories = [['https://ss3.4sqi.net/img/categories_v2/food/bbqalt_120.png', 'https://ss3.4sqi.net/img/categories_v2/food/burger_120.png', 'https://ss3.4sqi.net/img/categories_v2/food/fastfood_120.png'], ['https://ss3.4sqi.net/img/categories_v2/food/mediterranean_120.png'], ['https://ss3.4sqi.net/img/categories_v2/food/coffeeshop_120.png', 'https://ss3.4sqi.net/img/categories_v2/food/icecream_120.png', 'https://ss3.4sqi.net/img/categories_v2/food/default_120.png'], ['https://ss3.4sqi.net/img/categories_v2/food/pizza_120.png', 'https://ss3.4sqi.net/img/categories_v2/food/fastfood_120.png', 'https://ss3.4sqi.net/img/categories_v2/food/deli_120.png'], ['https://ss3.4sqi.net/img/categories_v2/food/middleeastern_120.png', 'https://ss3.4sqi.net/img/categories_v2/food/turkish_120.png'], ['https://ss3.4sqi.net/img/categories_v2/parks_outdoors/beach_120.png'], ['https://ss3.4sqi.net/img/categories_v2/nightlife/pub_120.png'], ['https://ss3.4sqi.net/img/categories_v2/nightlife/pub_120.png', 'https://ss3.4sqi.net/img/categories_v2/food/default_120.png'], ['https://ss3.4sqi.net/img/categories_v2/food/bakery_120.png'], ['https://ss3.4sqi.net/img/categories_v2/food/deli_120.png']]
                # print(categories)

                for i in range(len(dadesLlocs)):
                    print("dadesLlocs i", i)
                    # Definim tots els components de la card
                    if 'address' in dadesLlocs[i]["location"]: #! BUG-6
                        subtitle_card = Column(horizontal_alignment="center", controls=[
                            Text(f"Direcció: {dadesLlocs[i]["location"]['address']} | Distància: {dadesLlocs[i]["distance"]}m", color="white",weight=FontWeight.W_900),
                            Row(alignment="center",width = page.width, controls=[])
                            ]) #! Fer que sigui responsive row per si la pantalla es més petita
                    else: 
                        subtitle_card = Column(horizontal_alignment="center", controls=[
                            Text(f"Direcció: {None} | Distància: {dadesLlocs[i]["distance"]}m", color="white",weight=FontWeight.W_900),
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
                                                f"{dadesLlocs[i]["name"]}",  
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
                    if images_request[i] != []: #! BUG-6
                        print("Si té fotos")
                        if len(dadesLlocs[i]['photos']) == 2: 
                            print("prova")
                            img_principal = Row(alignment="center",controls=[AnimatedSwitcher(transition=AnimatedSwitcherTransition.FADE,duration=500,content=Image(
                                    animate_opacity=250,
                                    border_radius=15,
                                    src=images_request[index_photo_stack][0], #URL imatge
                                    width = page.width * 0.8, 
                                    height = page.height * 0.8 * 0.65, 
                                    fit="COVER"
                                    ))])
                        else: 
                                img_principal = Row(alignment="center",controls=[AnimatedSwitcher(transition=AnimatedSwitcherTransition.FADE,duration=500,content=Image(
                                    animate_opacity=250,
                                    border_radius=15,
                                    src=images_request[index_photo_stack][0], #URL imatge
                                    width = page.width * 0.8, 
                                    height = page.height * 0.8 * 0.65, 
                                    fit="COVER"
                                    ))])
                                img_esq =Image(
                                        animate_opacity=250,
                                        left=-page.width * 0.75,
                                        top=35,                                     # ! BUG-8
                                        src=images_request[index_photo_stack][len(images_request[index_photo_stack]) - 1],#URL imatge
                                        border_radius=20,
                                        width = page.width * 0.8, 
                                        height = page.height * 0.8 * 0.55, 
                                        fit="COVER",
                                    )
                                img_dret = Image(
                                        animate_opacity=250,
                                        right=-page.width * 0.75,
                                        top=35,
                                        src=images_request[index_photo_stack][1],#URL imatge
                                        border_radius=15,
                                        width = page.width * 0.8, 
                                        height = page.height * 0.8 * 0.55, 
                                        fit="COVER",
                                    )
                    else:
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
                        await asyncio.sleep(0.25) 
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
                        await asyncio.sleep(0.25) 
                        img_principal.src = images_request[index_photo_stack][index_photo] 
                        img_principal.opacity = 1
                        img_esq.src = images_request[index_photo_stack][index_photo-1 if index_photo-1 >= 0 else (len(images_request[index_photo_stack])-1)]  
                        img_dret.src = images_request[index_photo_stack][index_photo+1 if index_photo+1 <= (len(images_request[index_photo_stack])- 1) else 0]  
                        page.update()
                    
                    print("Carta creada")
                    carta = Container(
                            image_src = "https://i.imgur.com/Kc6KkMt.jpeg",
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
                        on_horizontal_drag_end=lambda e: handle_swipe(e),
                        on_vertical_drag_end=lambda e: handle_swipe_vertical(e)
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