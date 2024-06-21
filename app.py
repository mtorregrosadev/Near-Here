import flet 
from flet import Page,Geolocator, ImageFit, ImageRepeat,Card,GridView, ListTile, MainAxisAlignment,TextButton,Stack,Column,TextSpan,TextStyle,Paint,AlertDialog,IconButton, StrokeJoin,PaintingStyle,ShadowBlurStyle, BoxShadow, Image, ListTile,GestureDetector, FontWeight,ElevatedButton, Dismissible,DismissDirection, SafeArea,Theme, animation, Container, transform, Icon, icons, colors, alignment, icons, Row, Text, ResponsiveRow, Chip, NavigationBarDestination, NavigationBar 
from math import pi
import asyncio
import json
import location
anterior = 1
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
    }
    page.theme = Theme(font_family="Helvetica Neue")
    #gl = Geolocator()
    #page.add(gl)
    #gl.request_permission() 
    #location.handle_permission(gl,AlertDialog, page, Text,TextButton,MainAxisAlignment)
    page.update()

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
        cards[0].animate_scale = animation.Animation(600)
        cards[0].scale = 2
        cards[0].opacity = 0.1
        botons.animate_opacity = animation.Animation(600)
        Tags_amunt.animate_opacity = animation.Animation(600)
        botons.opacity = 0.12
        Tags_amunt.opacity = 0.12
        page.update()
        await asyncio.sleep(0.6)
        stack_cards.visible = False
        botons.visible = False
        Tags_amunt.visible = False
        page.update()
        #Comença a afegir l'altre pàgina
        #page.add(tornar)

    
    size_title = (page.height * 0.04) - 7
    
    nom_del_restaurant = Stack(
        alignment=alignment.center,
        height=page.height * 0.055,
        width=page.width,
        controls=[
            Container(
                content=Text(
                    text_align="center", 
                    spans=[
                        TextSpan(
                            "Nom del restaurant!",  
                            TextStyle(
                                size=size_title,
                                weight=FontWeight.W_900,
                                font_family="Stres",
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
                    spans=[
                        TextSpan(
                            "Nom del restaurant!",
                            TextStyle(
                                size=size_title, 
                                weight=FontWeight.W_900,
                                font_family="Stres",
                                color=colors.BLACK,
                            ),
                        ),
                    ],
                ),
                alignment=alignment.center
            ),
        ],
    )

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
                        subtitle=Text(f"No se sffsd sdf  jksf  hf kdjshf khfjdksh fsjkfh djks fjdksf", color="white",text_align="center",font_family="Helvetica Neue",weight=FontWeight.W_900),
                        height=(page.height * 0.8) * 0.15  
                        ),
                    Image(
                        src=f"https://picsum.photos/{round(page.width * 0.92)}/{round((page.height * 0.8)* 0.65)}",
                        border_radius = 15+((page.height*0.8)*0.16),
                        width = page.width * 0.92, 
                        height = page.height * 0.8 * 0.65,
                        filter_quality="HIGH"
                        )
                    ]
                )
                        
        )
    ]
    
    def restaurants_select(e):
        pass
    
#Definirem aqui tots els components com a variables per a tal d'accedir-hi en qualsevol moment en el programa
    Tags_amunt =Row( #Totes les etiquetes juntes 
                spacing=10,
                alignment= "center",
                scale=0.91,
                controls=[
                    Chip(
                        selected_color="#AAD7D9",
                        bgcolor="#E8EEED",
                        label=Text("Restaurants"),
                        on_select=restaurants_select
                    ), 
                    Chip(
                        selected_color="#AAD7D9",
                        bgcolor="#E8EEED",
                        label=Text("Llocs emblematics"),
                        on_select=restaurants_select
                    ), 
                    Chip(
                        selected_color="#AAD7D9",
                        bgcolor="#E8EEED",
                        label=Text("Ns"),
                        on_select=restaurants_select
                    ),
                    Chip(
                        selected_color="#AAD7D9",
                        bgcolor="#E8EEED",
                        label=Text("Restaurants"),
                        on_select=restaurants_select
                    ), 
                    Chip(
                        selected_color="#AAD7D9",  
                        bgcolor="#E8EEED",                 
                        label=Text("Llocs emblematics"),
                        on_select=restaurants_select
                    ), 
                    Chip(
                        selected_color="#AAD7D9",                    
                        bgcolor="#E8EEED",
                        label=Text("Ns"),
                        on_select=restaurants_select
                    )
                ],
                scroll="always",
    )
    
    size_botons = page.width / 30
    if size_botons >= 14:
        size_botons = 14
    botons = ResponsiveRow( #Aqui van tots els botons junts 
            vertical_alignment="end",
            controls=[
                ElevatedButton(content=Text("Següent", size=size_botons),on_click=seguent, bgcolor="#d9acaa", color="black",col=4), 
                ElevatedButton(content=Text("Més info", size=size_botons), on_click=mes_info,bgcolor="#FBF9F1",color="black",col=4),
                ElevatedButton(content=Text("Guarda!", size=size_botons), on_click=guarda, bgcolor="#aad9c4",color="black",col=4), 
    ]) 
    stack_cards = Stack(alignment=alignment.center, offset=(0,0), expand = True)
    configuracio =Card(color = "#AAD7D9", height=page.height * 0.8,
            content=Container(
                content=Column(
                    [
                        ListTile(
                            title=Text("Configuració", size = 20, weight=FontWeight.W_500),
                        ),
                        ListTile(title=Text("General"), dense=True),
                        ListTile(
                            leading=Icon(icons.PALETTE_OUTLINED, color="black"),
                            trailing = Icon(icons.CHEVRON_RIGHT_OUTLINED),
                            title=Text("Tema", color="black"),
                            selected=True,
                            # on_click=hey
                        ),
                        ListTile(
                            leading=Icon(icons.LANGUAGE, color="black"),
                            trailing = Icon(icons.CHEVRON_RIGHT_OUTLINED),
                            title=Text("Idioma", color="black"),
                            selected=True,
                            # on_click=hey
                        ),
                        ListTile(
                            leading=Icon(icons.HISTORY, color="black"),
                            trailing = Icon(icons.CHEVRON_RIGHT_OUTLINED),
                            title=Text("Historial de llocs", color="black"),
                            selected=True,
                            # on_click=hey
                        ),
                    ],
                    spacing=0,
                ),
            )
        )
    
    configuracio = SafeArea(content=configuracio)

    saved_cards = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,345,435,4,543] # Suposem que tenim ja la variable i la deixem 
    images_saved = GridView(
        expand=True,
        runs_count=3,
        child_aspect_ratio=1,
        spacing=5,
        run_spacing=5,
    )
    
    async def canvi_des_de_llocs():
            stack_cards.visible = False
            botons.visible = False
            Tags_amunt.visible = False
            page.update() 
    async def canvi_des_de_favorits():
        page.remove(images_saved)
        page.update()
    async def canvi_des_de_configuracio():
        page.remove(configuracio)
        page.update()
    
    async def changetab(e):
        global anterior
        index = e.control.selected_index
        if index == 1: #Llocs
            if anterior == 0:
                await canvi_des_de_favorits()
            elif anterior == 2:
                await canvi_des_de_configuracio()
            anterior = index
            print("Seleccionat llocs!")
            selected_llocs.offset = transform.Offset(0,0)
            botons.visible = True
            stack_cards.visible = True
            Tags_amunt.visible = True
            botons.opacity = 1
            Tags_amunt.opacity = 1
            stack_cards.opacity = 1
            selected_llocs.offset = transform.Offset(0, -0.25)
            page.update()
            await asyncio.sleep(0.14)
            selected_llocs.offset = transform.Offset(0,0)
            page.update()       
            
        elif index == 0: #Favorits
            if anterior == 1:
                await canvi_des_de_llocs()
            elif anterior == 2:
                await canvi_des_de_configuracio()
            anterior = index
            print("Favorits seleccionat")
            images_saved.controls = []
            page.add(images_saved)
            for i in range(len(saved_cards)):
                images_saved.controls.append(
                    Image(
                        src=f"https://picsum.photos/150/150?{i}",
                        border_radius=10,
                ))
                page.update()
             
            while index == 0: #Animacions icones
                await asyncio.sleep(1)
                selected_favorits.size = 27 if selected_favorits.size == 24 else 24
                page.update()
                index = e.control.selected_index #S'ha d'actualitzar a dins del codi la variable index, ja que sinó sempre sera True

        elif index == 2: #Configuració
            if anterior == 1:
                await canvi_des_de_llocs()
            elif anterior == 0:
                await canvi_des_de_favorits()
            anterior = index
            configuracio.visible = True
            print("Configuració seleccionada")
            await asyncio.sleep(0.01)
            selected_configuracio.rotate.angle += (2*pi)
            page.update()
            page.add(configuracio)
            
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
    Tags_amunt.height = page.height * 0.05
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
                    cards.append(Container(
                        image_src = "https://i.imgur.com/Kc6KkMt.jpeg",
                        image_fit = "FILL",
                        offset=(0,0),
                        border_radius=15, 
                        width = page.width,
                        height = page.height * 0.8,
                        animate_offset=animation.Animation(500),
                        scale=0,
                        animate_scale=animation.Animation(340, "easeOutSine"),
                        content=Column(
                            horizontal_alignment="center",
                            controls=[
                                ListTile(
                                    title=nom_del_restaurant,
                                    subtitle=Text(f"No se sffsd sdf  jksf  hf kdjshf khfjdksh fsjkfh djks fjdksf", color="white",text_align="center",font_family="Helvetica Neue",weight=FontWeight.W_900),
                                    height=(page.height * 0.8) * 0.15  
                                    ),
                                Image(
                                    src=f"https://picsum.photos/{round(page.width * 0.92)}/{round((page.height * 0.8 )* 0.65)}",
                                    border_radius = 15+((page.height*0.8)*0.16),
                                    width = page.width * 0.92, 
                                    height = page.height * 0.8 * 0.65,
                                    filter_quality="HIGH"
                                    )
                                ]
                            )
                                    
            ))   
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

    Tags_amunt = SafeArea(content=Tags_amunt)
    page.add(
        Tags_amunt,
        stack_cards,
        botons, 
    )
    
    
flet.app(target=main,assets_dir="assets")