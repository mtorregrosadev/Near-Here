import flet 
from flet import Page, ElevatedButton, SafeArea,ScrollbarTheme,Theme,MaterialState, animation, Container, transform, Icon, icons, colors,Divider, alignment, IconButton, icons, Row, Text, ResponsiveRow, RoundedRectangleBorder, Chip, TextField, NavigationDestination, NavigationBar,NavigationBarLabelBehavior 
import time
from math import pi

def main(page: Page):
    page.title = "Near here..."
    page.window_width = 600
    page.window_height = 800
    page.horizontal_alignment = "center"
    #page.vertical_alignment ="end"
    page.theme_mode = "light"

    page.fonts = {
           "Outfit": "fonts/Outfit.ttf",
    }
    page.theme = Theme(font_family="Outfit")
    page.update()

    def animate_left(e):
        if contenidor2.visible == False:
            contenidor2.offset = transform.Offset(0,0)
            contenidor.offset = transform.Offset(-4,0) #Aquest el que fa es moure de lloc l'element
            page.update()
            time.sleep(0.3)
            contenidor.visible = False
            contenidor2.visible = True
            page.update()
            time.sleep(0.2)
            contenidor2.scale = 1
            contenidor.scale= 0
            page.update()
        
        elif contenidor.visible == False:
            contenidor.offset = transform.Offset(0,0)
            contenidor2.offset = transform.Offset(-4,0) #Aquest el que fa es moure de lloc l'element
            page.update()
            time.sleep(0.3)
            contenidor2.visible = False
            contenidor.visible = True
            page.update()
            time.sleep(0.2)
            contenidor.scale = 1
            contenidor2.scale= 0
            page.update()
    
    def animate_right(e):
        if contenidor2.visible == False:
            contenidor2.offset = transform.Offset(0,0)
            contenidor.offset = transform.Offset(4,0) #Aquest el que fa es moure de lloc l'element
            page.update()
            time.sleep(0.3)
            contenidor.visible = False
            contenidor2.visible = True
            page.update()
            time.sleep(0.2)
            contenidor2.scale = 1
            contenidor.scale= 0
            page.update()

        elif contenidor.visible == False: 
            contenidor.offset = transform.Offset(0,0)
            contenidor2.offset = transform.Offset(4,0) #Aquest el que fa es moure de lloc l'element
            page.update()
            time.sleep(0.3)
            contenidor2.visible = False
            contenidor.visible = True
            page.update()
            time.sleep(0.2)
            contenidor.scale = 1
            contenidor2.scale= 0
            page.update()

    def animate_center(e):
        contenidor.offset = transform.Offset(0,0) #Aquest el que fa es moure de lloc l'element
        contenidor.update()
           
    contenidor = Container(
        bgcolor="#86A3B8", 
        offset=(0,0),
        border_radius=40, 
        expand_loose=True,
        animate_offset=animation.Animation(500),
        scale=1,
        animate_scale=animation.Animation(450, "easeOutSine")
    )
    contenidor2 = Container(
        bgcolor="#AAD7D9",
        border_radius=40,
        animate_offset=animation.Animation(500),
        scale=0,
        animate_scale=animation.Animation(450, "easeOutSine"), 
        visible=False
    )
    
    def restaurants_select(e):
        pass
    
    divider = Divider(height=30, thickness=0.1)
    
#Definirem aqui tots els components com a variables per a tal d'accedir-hi en qualsevol moment en el programa
    Tags_amunt =Row( #Totes les etiquetes juntes 
                spacing=10,
                alignment= "center",
                scale=0.91,
                controls=[
                    Chip(
                        selected_color="#E5E1DA",
                        label=Text("Restaurants"),
                        on_select=restaurants_select
                    ), 
                    Chip(
                        selected_color="#E5E1DA",
                        label=Text("Llocs emblematics"),
                        on_select=restaurants_select
                    ), 
                    Chip(
                        selected_color="#E5E1DA",
                        label=Text("Ns"),
                        on_select=restaurants_select
                    ),
                    Chip(
                        selected_color="#E5E1DA",
                        label=Text("Restaurants"),
                        on_select=restaurants_select
                    ), 
                    Chip(
                        selected_color="#E5E1DA",                   
                        label=Text("Llocs emblematics"),
                        on_select=restaurants_select
                    ), 
                    Chip(
                        selected_color="#E5E1DA",                    
                        label=Text("Ns"),
                        on_select=restaurants_select
                    )
                ],
                scroll="always",
            )
    contenidors = ResponsiveRow( #Aqui van tots els contenidors junts 
            offset=(0,0),
            expand = 18,
            expand_loose=True,
            height=560,
            width=500,
            controls=[
                contenidor,
                contenidor2,
            ]
        )
    botons = ResponsiveRow( #Aqui van tots els botons junts 
            vertical_alignment="end",
            controls=[
            ElevatedButton("Seguent", on_click=animate_left, bgcolor="#d9acaa", col=4), 
            ElevatedButton("Més info", on_click=animate_center,bgcolor="#FBF9F1",col=4),
            ElevatedButton("Guarda!", on_click=animate_right, bgcolor="#aad9c4",col=4), 
    ]) 
    bt = Container(botons, bgcolor="red", expand=6)

    def changetab(e):
        index = e.control.selected_index
        if index == 1:
            print("Seleccionat llocs!")
            contenidors.visible == True
            Tags_amunt.visible == True
            botons.visible == True
            selected_llocs.offset = transform.Offset(0, -0.3)
            page.update()
            time.sleep(0.1)
            selected_llocs.offset = transform.Offset(0,0)
            page.update()

        elif index == 0:
            print("Favorits seleccionat")

            while index == 0: #Animacions icones
                time.sleep(1)
                selected_favorits.size = 27 if selected_favorits.size == 24 else 24
                page.update()

        elif index == 2:
            print("Configuració seleccionada")
            time.sleep(0.01)
            selected_configuracio.rotate.angle += (2*pi)
            page.update()
    
    selected_favorits =Icon(name=icons.FAVORITE_ROUNDED, color="#E78895", animate_size=200)
    selected_llocs =Icon(name=icons.LOCATION_PIN, color=colors.BLACK, animate_offset=140, offset=transform.Offset(0,0)) 
    selected_configuracio = Icon(name=icons.SETTINGS_ROUNDED, color=colors.BLACK, rotate=transform.Rotate(0, alignment=alignment.center), animate_rotation=animation.Animation(duration=1000, curve="bounceOut"))
    
    page.navigation_bar=NavigationBar(
        bgcolor = "#AAD7D9",
        adaptive=True,
        height=90,
        #label_behavior=NavigationBarLabelBehavior.ONLY_SHOW_SELECTED,
        selected_index = 1,
        indicator_color = "#FBF9F1",
        on_change=changetab,
        destinations=[
            NavigationDestination(label="Favorits", icon="FAVORITE_BORDER_ROUNDED", selected_icon_content=selected_favorits),
            NavigationDestination(label="Llocs", icon="LOCATION_ON_OUTLINED", selected_icon_content=selected_llocs), 
            NavigationDestination(label="Configuració", icon="SETTINGS_OUTLINED", selected_icon_content=selected_configuracio),
        ]
    )
    
    page.add(
        SafeArea(content=Tags_amunt, top=True),
        contenidors,
        bt
    )

flet.app(target=main,assets_dir="assets")