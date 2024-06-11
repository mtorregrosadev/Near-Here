import flet 
from flet import Page, Stack,Column,TextSpan,TextStyle,Paint, StrokeJoin,PaintingStyle,ShadowBlurStyle, BoxShadow, Image, ListTile,GestureDetector, FontWeight,ElevatedButton, Dismissible,DismissDirection, SafeArea,Theme, animation, Container, transform, Icon, icons, colors, alignment, icons, Row, Text, ResponsiveRow, Chip, NavigationDestination, NavigationBar 
import time
from math import pi
import asyncio
import json

def main(page: Page):
    page.bgcolor = "#FFFCF1"
    page.title = "Near here..."
    page.window_width = 390
    page.window_height = 790
    page.horizontal_alignment = "center"
    page.theme_mode = "light"
    page.fonts = {
           "Proxima Nova": "fonts/ProximaNova-Regular.ttf",
           "Proxima Nova Bold": "fonts/ProximaNova-Bold.ttf",
           "Proxima Nova ExtraBold": "fonts/ProximaNova-ExtraBold.ttf",
           "Helvetica Neue": "fonts/HelveticaNeueMedium.otf",
           "Stres": "fonts/Stres.otf",
           "Abril Fatface": "http://themes.googleusercontent.com/static/fonts/abrilfatface/v5/X1g_KwGeBV3ajZIXQ9VnDibsRidxnYrfzLNRqJkHfFo.ttf",
    }
    page.theme = Theme(font_family="Helvetica Neue")
    page.update()

    async def animate_left(e):
        cards[0].animate_offset = animation.Animation(600)  
        cards[0].offset = transform.Offset(-4, 0)  
        page.update()
        await asyncio.sleep(0.2)  
        cards.remove(cards[0])
        print(f"Card {len(cards)} swiped left")
        update_cards()
        await scale_next_card()
    
    async def animate_right(e):
        cards[0].animate_offset = animation.Animation(600)  # Configura la animación de desplazamiento
        cards[0].offset = transform.Offset(4, 0)  # Aplica el desplazamiento
        page.update()
        await asyncio.sleep(0.2)  # Espera a que la animación termine
        cards.remove(cards[0])
        print(f"Card {len(cards)} swiped left")
        update_cards()
        await scale_next_card()

    async def animate_center(e):
        pass   
    
    size_title = (page.height * 0.04) - 7
    nom_del_restaurant = Stack(
        alignment=alignment.center,
        height=page.height * 0.057,
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
                                    stroke_width=5,
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
            width = page.width * 1,
            height = page.height * 0.8,
            animate_offset=animation.Animation(500),
            scale=0,
            animate_scale=animation.Animation(450, "easeOutSine"),
            content=Column(
                horizontal_alignment="center",
                controls=[
                    ListTile(
                        title=nom_del_restaurant,
                        subtitle=Text(f"No se sffsd sdf  jksf  hf kdjshf khfjdksh fsjkfh djks fjdksf", color="white",text_align="center",font_family="Helvetica Neue",weight=FontWeight.W_900),
                        height=(page.height * 0.8) * 0.15  
                        ),
                    Image(
                        src=f"https://picsum.photos/{round(page.width * 0.8)}/{round((page.height * 0.8 )* 0.65)}",
                        border_radius = 15+((page.height*0.8)*0.16),
                        width = page.width * 0.8, 
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
                ElevatedButton(content=Text("Següent", size=size_botons),on_click=animate_left, bgcolor="#d9acaa", color="black",col=4), 
                ElevatedButton(content=Text("Més info", size=size_botons), on_click=animate_center,bgcolor="#FBF9F1",color="black",col=4),
                ElevatedButton(content=Text("Guarda!", size=size_botons), on_click=animate_right, bgcolor="#aad9c4",color="black",col=4), 
    ]) 
    stack = Stack(alignment="center", offset=(0,0), expand = True)

    async def changetab(e):
        index = e.control.selected_index
     
        if index == 1: #Llocs
            print("Seleccionat llocs!")
            stack.visible == True
            Tags_amunt.visible == True
            botons.visible == True
            selected_llocs.offset = transform.Offset(0, -0.3)
            page.update()
            await asyncio.sleep(0.1)
            selected_llocs.offset = transform.Offset(0,0)
            page.update()

        elif index == 0: #Favorits
            while index == 0: #Animacions icones
                await asyncio.sleep(1)
                selected_favorits.size = 27 if selected_favorits.size == 24 else 24
                page.update()
                index = e.control.selected_index #S'ha d'actualitzar a dins del codi la variable index, ja que sinó sempre sera True
            print("Favorits seleccionat")

        elif index == 2: #Configuració
            print("Configuració seleccionada")
            await asyncio.sleep(0.01)
            selected_configuracio.rotate.angle += (2*pi)
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
            NavigationDestination(label="Favorits", icon="FAVORITE_BORDER_ROUNDED", selected_icon_content=selected_favorits),
            NavigationDestination(label="Llocs", icon="LOCATION_ON_OUTLINED", selected_icon_content=selected_llocs), 
            NavigationDestination(label="Configuració", icon="SETTINGS_OUTLINED", selected_icon_content=selected_configuracio),
        ]
    )
    
    botons.height = page.height * 0.08
    botons.width = page.width
    page.navigation_bar.height = page.height * 0.11
    Tags_amunt.height = page.height * 0.05
    Tags_amunt.width = page.width 
    stack.height = page.height * 0.8
    stack.width = page.width 
   
    async def on_swipe(e):
        data = json.loads(e.data)
        print(data["pv"])
        if data["pv"] != 0:
            if data["pv"] < 1: #Esquerra
                cards[0].animate_offset = animation.Animation(500)  
                cards[0].offset = transform.Offset(-4, 0)  
                page.update()
                await asyncio.sleep(0.15) 
                cards.remove(cards[0])
            elif data["pv"] > 0: #Dreta
                cards[0].animate_offset = animation.Animation(500)  
                cards[0].offset = transform.Offset(4, 0)  
                page.update()
                await asyncio.sleep(0.15)  
                cards.remove(cards[0])   
            update_cards()
            await scale_next_card()

    async def on_swipe_vertical(e):
        data = json.loads(e.data)
        print(e.data)
        print(data["pv"])
        if data["pv"] < 1 and data["vy"] < 0:
            cards[0].animate_scale = animation.Animation(800)
            cards[0].scale = 2
            cards[0].animate_opacity = animation.Animation(700)
            cards[0].opacity = 0.50 
            page.update()
            await asyncio.sleep(0.15)
            stack.visible = False
            botons.visible = False
            Tags_amunt.visible = False
            update_cards()
            await scale_next_card()


    def handle_swipe(e):
        asyncio.run(on_swipe(e))
    def handle_swipe_vertical(e):
        asyncio.run(on_swipe_vertical(e))
    # Aquest el que fa es convertir cada card individual en GestureDetector. Amb això, podem detectar cap a on es mou i com funciona. Es molt útil i ens ho serà en un futur.
    def update_cards():
        #print(cards[0].content.controls[1].image_src)
        stack.controls.clear()
        for card in cards:
            stack.controls.append(
                GestureDetector(
                    content=card,
                    on_horizontal_drag_end=lambda e: handle_swipe(e),
                    on_vertical_drag_end=lambda e: handle_swipe_vertical(e)
                )
            )
 
            if len(cards) == 1:
                for i in range(0,10):
                    cards.append(Container(
                        image_src = "https://i.imgur.com/Kc6KkMt.jpeg",
                        image_fit = "FILL",
                        offset=(0,0),
                        border_radius=15, 
                        width = page.width * 1,
                        height = page.height * 0.8,
                        animate_offset=animation.Animation(500),
                        scale=0,
                        animate_scale=animation.Animation(450, "easeOutSine"),
                        content=Column(
                            horizontal_alignment="center",
                            controls=[
                                ListTile(
                                    title=nom_del_restaurant,
                                    subtitle=Text(f"No se sffsd sdf  jksf  hf kdjshf khfjdksh fsjkfh djks fjdksf", color="white",text_align="center",font_family="Helvetica Neue",weight=FontWeight.W_900),
                                    height=(page.height * 0.8) * 0.15  
                                    ),
                                Image(
                                    src=f"https://picsum.photos/{round(page.width * 0.8)}/{round((page.height * 0.8 )* 0.65)}",
                                    border_radius = 15+((page.height*0.8)*0.16),
                                    width = page.width * 0.8, 
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
        if len(cards) > 1:  
            next_card = cards[0]
            next_card.scale = 0
            page.update()
            await asyncio.sleep(0.4)  
            next_card.scale = 1
            page.update()

    Tags_amunt = SafeArea(content=Tags_amunt)
    page.add(
        Tags_amunt,
        stack,
        botons, 
    )

flet.app(target=main,assets_dir="assets")