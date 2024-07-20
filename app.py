import flet 
from flet import Page,View,border, RoundedRectangleBorder, Geolocator,ImageFit,BorderRadius,AnimatedSwitcherTransition,AppBar,Card,GridView,TextThemeStyle,ListTile, MainAxisAlignment,AnimatedSwitcher,Stack,Column,TextSpan,TextStyle,Paint,AlertDialog,IconButton, StrokeJoin,PaintingStyle,ShadowBlurStyle, BoxShadow, Image, ListTile,GestureDetector, FontWeight,ElevatedButton, Dismissible,DismissDirection, SafeArea,Theme, animation, Container, transform, Icon, icons, colors, alignment, icons, Row, Text, ResponsiveRow, Chip, NavigationBarDestination, NavigationBar 
from math import pi
import asyncio
import json
import location
import random
index_photo = 0
index = 0
def main(page: Page):
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
           "Helvetica Neue": "fonts/HelveticaNeueMedium.otf",
           "Stres": "fonts/Stres.otf",
           "WorkSans": "fonts/WorkSans-Black.ttf"
    }
    page.theme = Theme(font_family="Helvetica Neue")
    #gl = Geolocator()
    #page.add(gl)
    #gl.request_permission() 
    #location.handle_permission(gl,AlertDialog, page, Text,TextButton,MainAxisAlignment)
    page.update()
    categories_sel = []

    def view_pop(event): #Per anar enrere 
        print("view pop:", event.view) #Això només imprimeix en terminal, de normal no cal
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
            page.views.append(View(controls=[AppBar(title=Text("Historial de Llocs"), bgcolor="#AAD7D9"), images_saved],bgcolor = "#FFFCF1"))
            images_saved.controls = []
            if len(loc_visited) > 0:
                for i in range(len(loc_visited)):
                    images_saved.controls.append(
                        Container(content=Column(spacing=0.5,horizontal_alignment="center", controls=[Image(
                            src=f"https://picsum.photos/150/150?{i}",
                            border_radius=10), Text(f"{i}", text_align="center")
                    ])))
                    page.update()
            else:
                page.views.append(View(controls=[AppBar(title=Text("Historial de Llocs"), bgcolor="#AAD7D9"),SafeArea(content=Text("No has explorat cap lloc encara!", text_align="center", height=page.height))], bgcolor = "#FFFCF1"))
        
        if page.route == '/configuracio/tema':
            page.views.append(View(controls=[AppBar(title=Text("Tema"), bgcolor="#AAD7D9")]))

        if page.route == '/configuracio/idioma':
            page.views.append(View(controls=[AppBar(title=Text("Idioma"), bgcolor="#AAD7D9")]))

        if page.route == "/configuracio/config_near":
            page.views.append(View(controls=[AppBar(title=Text("Pàrametres cerca"), bgcolor="#AAD7D9")]))

        if page.route == '/info':
            page.add(SafeArea(content=ElevatedButton("Tornar", on_click=tornar)))
        
        if page.route == '/categories':
            page.add(SafeArea(content=ElevatedButton("Tornar", on_click=tornar)))
        
        page.update()

    page.on_route_change = on_change_page #Aquest defineix que volem que faci el programa en el canvi de route 
    page.on_view_pop = view_pop
    async def seguent(e):
        cards[0].offset = transform.Offset(-4, 0)  
        page.update()
        await asyncio.sleep(0.15)  
        cards.remove(cards[0])
        print(f"Card {len(cards)} swiped left")
        update_cards()
        await scale_next_card()
    
    async def guarda(e):
        cards[0].offset = transform.Offset(4, 0)  
        page.update()
        await asyncio.sleep(0.15)  
        cards.remove(cards[0])
        print(f"Card {len(cards)} swiped left")
        update_cards()
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

    size_title = (page.height * 0.04) - 7
    
    nom_del_restaurant = Stack(
        alignment=alignment.center,
        height=page.height * 0.055,
        width=page.width,
        controls=[
            Container(
                content=Text(
                    text_align="center", 
                    theme_style=TextThemeStyle.HEADLINE_LARGE,
                    width=page.width * 0.9,
                    height=page.height * 0.05,
                    spans=[
                        TextSpan(
                            "Nom del restaurant!",  
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
                    text_align="center",
                    theme_style=TextThemeStyle.HEADLINE_LARGE,
                    width=page.width * 0.9,
                    height=page.height * 0.05,
                    spans=[
                        TextSpan(
                            "Nom del restaurant!",
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
    
    images_request=[ #Aqui aniran totes les fotos obtingudes per l'API
            f"https://images.unsplash.com/photo-1714891203404-b25f32706e0a?q=80&w={round(page.width * 0.8)}&h={round((page.height * 0.8) * 0.65)}&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
            f"https://images.unsplash.com/photo-1714837291207-4985c06c9a60?q=80&w={round(page.width * 0.8)}&h={round((page.height * 0.8) * 0.65)}&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
            f"https://images.unsplash.com/photo-1715109429876-e00fbe6c4ae3?q=80&w={round(page.width * 0.8)}&h={round((page.height * 0.8) * 0.65)}&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
            f"https://plus.unsplash.com/premium_photo-1714115035000-023149febb01?q=80&w={round(page.width * 0.8)}&h={round((page.height * 0.8) * 0.65)}&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
            f"https://images.unsplash.com/photo-1714836992953-b8f7b4dc8afc?q=80&w={round(page.width * 0.8)}&h={round((page.height * 0.8) * 0.65)}&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    ]
    img_principal = Row(alignment="center",controls=[AnimatedSwitcher(transition=AnimatedSwitcherTransition.FADE,duration=500,content=Image(
        border_radius=15,
        src=images_request[0], #URL imatge
        width = page.width * 0.8, 
        height = page.height * 0.8 * 0.65, 
        fit="FILL",
    ))])
    img_esq =Image(
            left=-page.width * 0.75,
            top=35,
            src=images_request[len(images_request) - 1],#URL imatge
            border_radius=20,
            fit="FILL",
    )
    img_dret = Image(
        right=-page.width * 0.75,
        top=35,
        src=images_request[1],#URL imatge
        border_radius=15,
        fit="FILL",
    )

    async def esq(e): #Detecta que has fet click a l'esquerra 
        global index_photo
        if index_photo <= 0:
            index_photo = len(images_request) - 1 # Fa que sempre l'index sigui un número a dins de la llista i resta un, fent així que puguem navegar
        else:
            index_photo -= 1
        img_principal.controls[0].content.src = images_request[index_photo] #Actualitza les fotos 
        img_esq.src = images_request[index_photo-1 if index_photo-1 >= 0 else (len(images_request)-1)]  #Resta un en el cas que sigui a dins de la llista, sinó posa el més gran (len) - 1, ja que contem des de 0
        # Incís: Mai entendre perquè els programadors contem des de 0, i després quan fas la longitud d'una llista conta des de 1, en fi.
        img_dret.src = images_request[index_photo+1 if index_photo+1 <= (len(images_request)- 1) else 0] #El mateix, detecta que sigui a dins de la llista i no sigui negatiu, en el cas posa 0
        page.update()

    async def dret(e): #Mateixos comentaris pero al reves
        global index_photo
        if index_photo >= (len(images_request)- 1):
            index_photo = 0
        else:
            index_photo += 1
        img_principal.controls[0].content.src = images_request[index_photo]
        img_esq.src = images_request[index_photo-1 if index_photo-1 >= 0 else (len(images_request)-1)]  
        img_dret.src = images_request[index_photo+1 if index_photo+1 <= (len(images_request)- 1) else 0]  
        page.update()
        
    cards = [
        Container(
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
                        subtitle=Column(horizontal_alignment="center", controls=[Text(f"Direcció: {None}, Distància: {None}", color="white",weight=FontWeight.W_900),Row(alignment="center",controls=[Text("Hey", color="white",weight=FontWeight.W_900)])]),
                        height=(page.height * 0.8) * 0.16  
                        ),
                        Container(content=Stack(
                                        [   img_principal,
                                            
                                            img_dret,
                                            img_esq,
                                            IconButton(
                                                    icon=icons.CHEVRON_RIGHT,
                                                    icon_color = "black",
                                                    bgcolor="#FBF9F1",
                                                    on_click=dret,
                                                    alignment=alignment.center,
                                                    right=2,
                                                    width = page.window.width * 0.1,
                                                    top=page.window.height * 0.8 * 0.7 / 2,
                                            ),
                                            IconButton(
                                                    icon=icons.CHEVRON_LEFT,
                                                    icon_color = "black",
                                                    bgcolor="#FBF9F1",
                                                    on_click=esq,
                                                    width = page.window.width * 0.1,
                                                    left=2,
                                                    top=page.window.height * 0.8 * 0.7 / 2,
                                            ),
                                        ]
                                    ),
                                    expand_loose=True,
                                   # bgcolor="black",
                                    #alignment=alignment.center,
                                    #padding=10,
                                    width=page.window.width,
                                    height=page.window.height * 0.8 * 0.65,
                                )
                    ]
                )
                        
        )
    ]
    
    def categ_chip_sel(e):
        if e.control.selected:# El que fa es afegir en el cas de que estigui seleccionat i detecta la chip
            categories_sel.append(13065) if e.control.label.value == "Restaurants" and e.control.selected else False
            categories_sel.append(16032) if e.control.label.value == "Parcs" and e.control.selected else False
            #categories_sel.append(16032) if e.control.label.value == "Parcs" and e.control.selected else False
        else:
            for category in categories_sel:
                if category == 13065 and e.control.label.value == "Restaurants": # Posar totes les condicions aqui
                    categories_sel.remove(category)
                if category == 16032 and e.control.label.value == "Parcs": # Posar totes les condicions aqui
                    categories_sel.remove(category)
            
        print(categories_sel)
    def mes_info_select(e):
        page.go('/categories')
        Tags_amunt.controls[len(Tags_amunt.controls)-1].selected = False

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
                        label=Text("Restaurants",weight=FontWeight.W_400,font_family="default"),
                        leading=Icon(icons.RESTAURANT_MENU_OUTLINED),
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
                scroll="ADAPTIVE",
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
    loc_visited = [1,2,2,2,32,3,213,2,34,3,4,4,32,4,23,4,3,45,5,43,5,34,23,43,24,23,234,32,4,34]
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
    def update_cards():
        stack_cards.controls.clear()
        for card in cards:
            stack_cards.controls.append(
                GestureDetector(
                    content=card,
                    on_horizontal_drag_end=lambda e: handle_swipe(e),
                    on_vertical_drag_end=lambda e: handle_swipe_vertical(e)
                )
            )
 
            if len(cards) == 1:
                for i in range(0,2):
                    cards.append( 
                        Container(
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
                                        subtitle=Column(horizontal_alignment="center", controls=[Text(f"Direcció: {None}, Distància: {None}", color="white",weight=FontWeight.W_900),Row(alignment="center",controls=[Text("Hey", color="white",weight=FontWeight.W_900)])]),
                                        height=(page.height * 0.8) * 0.16  
                                        ),
                                        Container(content=Stack(
                                                        [   
                                                            Row(alignment="center",controls=[Image(
                                                                border_radius=15,
                                                                src=f"https://picsum.photos/{round(page.width * 0.8)}/{round((page.height * 0.8)* 0.65)}", 
                                                                width = page.width * 0.8, 
                                                                height = page.height * 0.8 * 0.65, 
                                                                fit="FILL",
                                                                expand_loose=True,
                                                            )]),
                                                            Image(
                                                                left=-page.width * 0.75,
                                                                src=f"https://picsum.photos/{round(page.width * 0.8)}/{round((page.height * 0.8)* 0.5)}",
                                                                border_radius=15,
                                                                fit="FILL",
                                                                top=35,
                                                                expand_loose=True,
                                                            ),
                                                            Image(
                                                                right=-page.width * 0.75,
                                                                src=f"https://picsum.photos/{round(page.width * 0.8)}/{round((page.height * 0.8)* 0.5)}",
                                                                border_radius=15,
                                                                fit="FILL",
                                                                top=35,
                                                                expand_loose=True,
                                                            ),
                                                            IconButton(
                                                                    icon=icons.CHEVRON_RIGHT,
                                                                    icon_color = "black",
                                                                    bgcolor="white",
                                                                    on_click=dret,
                                                                    alignment=alignment.center,
                                                                    right=0,
                                                                    width = page.window.width * 0.1,
                                                                    top=page.window.height * 0.8 * 0.7 / 2,
                                                            ),
                                                            IconButton(
                                                                    icon=icons.CHEVRON_LEFT,
                                                                    icon_color = "black",
                                                                    bgcolor="white",
                                                                    on_click=esq,
                                                                    width = page.window.width * 0.1,
                                                                    left=0,
                                                                    top=page.window.height * 0.8 * 0.7 / 2,
                                                            ),
                                                        ]
                                                    ),
                                                    expand_loose=True,
                                                    width=page.window.width,
                                                    height=page.window.height * 0.8 * 0.65,
                                                )
                                    ]
                                )
                                        
                        )
                    
                    )   
            page.update()
    
    update_cards()
    #L'iniciem només començar el programa per tal de fer apareixer tots els elements i escalem la primera a 1 per tal de mostrar-la
    cards[0].scale = 1 
    
    async def scale_next_card():
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
    
    
flet.app(target=main,assets_dir="assets")