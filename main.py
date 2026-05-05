import flet 
from flet import Page,CircleAvatar,RadioGroup,Radio,PagePlatform,LinearGradient,alignment,GradientTileMode,Markdown,Dropdown,ListView,TextField,DecorationImage,Dropdown,InteractiveViewer,Margin,TextButton,Divider,View,Border,Slider,BorderRadius,BorderRadius,Checkbox,RoundedRectangleBorder,TileAffinity,ExpansionTile,AnimatedSwitcherTransition,AppBar,Card,GridView,TextThemeStyle,ListTile, MainAxisAlignment,AnimatedSwitcher,Stack,Column,TextSpan,TextStyle,Paint,AlertDialog,IconButton, StrokeJoin,PaintingStyle, BoxShadow, Image, ListTile,GestureDetector, FontWeight,ElevatedButton, SafeArea,Theme, Animation, Container, Icon, Icons, Colors, Row, Text, ResponsiveRow, Chip, NavigationBarDestination, NavigationBar,BlurTileMode,Blur, Offset, Rotate, PageTransitionsTheme, PageTransitionTheme
import asyncio
from src.constants import *
from src.utils import resize_image_url, convertir_url

import json
import location
index_photo = 0
import requests
import random
import math
import httpx
from dotenv import load_dotenv 
import os 
from flet_geolocator import GeolocatorPermissionStatus, Geolocator
from flet_lottie import Lottie 
import sentry_sdk
import logging
import sys
from datetime import datetime
from src.api_handlers import LLocs_sostenibles, Llocs, Llocs_Yelp_info, Llocs_info, Llocs_yelp
from src.constants import CATEGORIES_LIST, get_system_instructions
from src.views.about import about_view
from src.views.info import info_view
from src.views.search_params import config_near_view
from src.views.settings import under_construction_view, ajuda_view, idioma_view, lloc_especific_view
from src.views.error import error_view
from src.views.favorits import favorits_view
from src.views.historial import historial_view
from src.views.categories import categories_view
from src.views.ia import ia_view_setup

load_dotenv()

# Configuracio del sistema de logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('near_here.log', encoding='utf-8')
    ]
)

# Silenciar els logs de debug de Flet
logging.getLogger('flet').setLevel(logging.WARNING)
logging.getLogger('flet_core').setLevel(logging.WARNING)
logging.getLogger('flet_runtime').setLevel(logging.WARNING)
logging.getLogger('flet_controls').setLevel(logging.WARNING)
logging.getLogger('flet_transport').setLevel(logging.WARNING)

logger = logging.getLogger('NearHere')

APP_SESSIONS = {}
CLIENT_STORAGES = {}

class MockClientStorage:
    def __init__(self, page):
        self.page = page
    
    async def set_async(self, key, value):
        CLIENT_STORAGES.setdefault(self.page, {})[key] = value
        
    async def get_async(self, key):
        return CLIENT_STORAGES.setdefault(self.page, {}).get(key)
        
    async def remove_async(self, key):
        if self.page in CLIENT_STORAGES and key in CLIENT_STORAGES[self.page]:
            del CLIENT_STORAGES[self.page][key]
            
    async def clear_async(self):
        if self.page in CLIENT_STORAGES:
            CLIENT_STORAGES[self.page].clear()
        
    async def get_keys_async(self, key_prefix):
        return list(CLIENT_STORAGES.setdefault(self.page, {}).keys())

def get_client_storage(page):
    if page not in CLIENT_STORAGES:
        CLIENT_STORAGES[page] = {}
        # We return a wrapper that has the async methods
    return MockClientStorage(page)


ai = 0
sostenible = True
images_request = []
index_photo_stack = -1
canvi = False
sostenible_2 = True
cards = []
 
import datetime

sentry_sdk.init(
    dsn=os.getenv('DSN_SENTRY'),
    # Add data like request headers and IP for users,
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii=True,
)

class MockGeolocator:
    async def get_permission_status(self):
        return GeolocatorPermissionStatus.WHILE_IN_USE

    async def request_permission(self):
        return GeolocatorPermissionStatus.WHILE_IN_USE
        
    async def get_current_position(self, configuration=None):
        from dataclasses import dataclass
        @dataclass
        class Position:
            latitude: float
            longitude: float
            accuracy: float = 0
            altitude: float = 0
            speed: float = 0
            
        return Position(latitude=41.471473, longitude=2.284979) # Example coord

async def main(page: Page):
    APP_SESSIONS.setdefault(page, {})

    if not hasattr(page, 'client_storage'):
        pass

        
    logger.info("========================================")
    logger.info("=== INICI DE L'APLICACIO NEAR HERE ===")
    logger.info("========================================")
    
    #crearem la splash screen
    splash = Container(
        content=Lottie(src='src/NearHere.json'),
        alignment=flet.Alignment.CENTER,
        bgcolor=Colors.WHITE,
        expand=True,
    )
    page.overlay.append(splash)
    page.update()

    logger.info("Configurant pagina inicial...")
    page.bgcolor = "#FFFCF1"
    page.title = "Near here..."
    page.window.width = 390
    page.window.height = 800
    page.horizontal_alignment = "center"
    page.theme_mode = "light"
    page.fonts = {
           "Helvetica Neue": "fonts/HelveticaNeue-Regular.otf",
           "WorkSans": "fonts/WorkSans-Black.ttf"
    }
    page.theme = Theme(
        font_family="Helvetica Neue",
        page_transitions=PageTransitionsTheme(
            android=PageTransitionTheme.NONE,
            ios=PageTransitionTheme.NONE,
            macos=PageTransitionTheme.NONE,
            linux=PageTransitionTheme.NONE,
            windows=PageTransitionTheme.NONE
        )
    )
    logger.info(f"Finestra configurada: {page.window.width}x{page.window.height}")
    
    # Use MockGeolocator to avoid "Unknown control" error on macOS desktop
    gl = MockGeolocator()
    # # page.overlay.append(gl) # Don't add mock to overlay
    page.update()
    APP_SESSIONS[page]["categories_sel"] = []
    APP_SESSIONS[page]["dadesLlocs"] = []
    APP_SESSIONS[page]["idioma"] = ""
    logger.info("Sessio inicialitzada amb valors per defecte")
    
    async def inicialitzar_configuracio():
        await get_client_storage(page).set_async("radius_sel", 1000)
        await get_client_storage(page).set_async("sort_sel", "RELEVANCE")
        await get_client_storage(page).set_async("preu", 0)
        logger.info("Configuracio inicialitzada: radius=1000m, sort=RELEVANCE, preu=0")

    async def inicialitzar_llistes():
        await get_client_storage(page).set_async("loc_visited", [])
        await get_client_storage(page).set_async("saved_cards", [])
        await get_client_storage(page).set_async("saved_cards_images", [])
        await get_client_storage(page).set_async("loc_visited_photos", [])  
        await get_client_storage(page).set_async("categories_visited", [])
        logger.info("Llistes inicialitzades (loc_visited, saved_cards, etc.)")

    async def configurar_ubicacio(gl):
        logger.info("Verificant permisos de geolocalitzacio...")
        status = await gl.get_permission_status()
        logger.info(f"Estat permisos: {status}")
        if str(status) == "GeolocatorPermissionStatus.WHILE_IN_USE" or str(status) == "GeolocatorPermissionStatus.ALWAYS":
            logger.info("Permisos de geolocalitzacio ja concedits")
        else:
            logger.warning("Permisos de geolocalitzacio no concedits - Sol·licitant...")
            await gl.request_permission()
            await location.handle_permission(gl, AlertDialog, page, Text, TextButton, MainAxisAlignment)

    logger.info("Inicialitzant configuracio i llistes...")
    await asyncio.gather(
        inicialitzar_configuracio(),
        inicialitzar_llistes(),
    )

    await asyncio.sleep(0.5)
    await configurar_ubicacio(gl)
    logger.info("Configuracio inicial completada")

    async def view_pop(event): #Per anar enrere 
        if page.route == '/categories' or page.route == '/info' or page.route == '/lloc_especific' or page.route == '/favorits':
            page.views.pop()
            await page.push_route('/')
        else: 
            page.views.pop()
            await page.push_route("/configuracio")
    async def on_change_page(e):
        page.theme.page_transitions.android = PageTransitionTheme.NONE
        page.theme.page_transitions.ios = PageTransitionTheme.NONE
        page.theme.page_transitions.macos = PageTransitionTheme.NONE
        page.theme.page_transitions.linux = PageTransitionTheme.NONE
        page.theme.page_transitions.windows = PageTransitionTheme.NONE
        Tags_amunt_safe = SafeArea(content=Tags_amunt)
        async def send_message(e):
            ia_container_TextField = ia_container.content.controls[0].content.controls[2].controls[1].value
            if ia_container_TextField == "":
                ia_container.content.controls[0].content.controls[2].controls[1].error_text = "Per enviar un missatge l'has d'escriure primer!"
                page.update()
            else:
                ia_container.content.controls[0].content.controls[2].controls[1].error_text = None
                ia_container.content.controls[0].content.controls[1].controls.append(
                    Container(bgcolor="#d1ddff",content=Row([Text(""), CircleAvatar(content=Icon(Icons.PERSON)), Markdown(f"{ia_container_TextField}",width=page.width*0.8)]))
                )
                ia_container.content.controls[0].content.controls[1].controls.append(Divider())
                ia_container.content.controls[0].content.controls[2].controls[1].value = ""
                ia_container.content.controls[0].content.controls[2].controls[2].focus()
                page.update()
                await asyncio.sleep(0.01)                      
                ia_container.content.controls[0].content.controls[1].controls.append(anim_carrega)
                page.update()
                await asyncio.sleep(0.1)
                history.append({"role": "user", "parts": [{"text": f"{ia_container_TextField}"}]})
                async with httpx.AsyncClient() as client:  # Crea una sessió asíncrona
                    response = await client.post(api, headers=headers, json=data)
                    if response.status_code == 200: 
                        resposta = response.json() 
                        resposta_100 = resposta['candidates'][0]['content']['parts'][0]['text']
                        ia_container.content.controls[0].content.controls[1].controls.append(
                            Container(bgcolor="#9796f0",content=Row([Text(""), CircleAvatar(content=Icon(Icons.PIN_DROP)), Markdown(f"{resposta_100}", width=page.width*0.8)]))
                        )
                        ia_container.content.controls[0].content.controls[1].controls.append(Divider())
                        ia_container.content.controls[0].content.controls[1].controls.remove(anim_carrega)
                        page.update()
        async def first_message():
            async with httpx.AsyncClient() as client:  # Crea una sessió asíncrona
                response = await client.post(api, headers=headers, json=data)  # Utilitza client.post() per fer la petició
                if response.status_code == 200:  # Comprova l'estat de la resposta
                    api_response = response.json()  # Espera la resposta JSON
                    chat_response = api_response['candidates'][0]['content']['parts'][0]['text']  # Accedeix al text de la resposta
                    ia_container.content.controls[0].content.controls[1].controls.remove(anim_carrega)
                    page.update()
                    ia_container.content.controls[0].content.controls[1].controls.append(Container(bgcolor="#9796f0", content=Row([Text(""), CircleAvatar(content=Icon(Icons.PIN_DROP)), Markdown(f"{chat_response}", width=page.width*0.8)]))) 
                    ia_container.content.controls[0].content.controls[1].controls.append(Divider())                   
                    page.update()
        async def exit_e(e):
            global ai 
            ai = 0
            page.overlay.remove(ia_container)
            await page.push_route('/')
            page.update()
        async def fullscreen(e):
            ia_container.content.controls[0].content.controls[0].height = page.height * 0.83 * 0.13 if ia_container.content.controls[0].height == page.height * 0.72 else page.height * 0.72 * 0.15
            ia_container.content.controls[0].content.controls[1].height = page.height * 0.83 * 0.65 if ia_container.content.controls[0].height == page.height * 0.72 else page.height * 0.72 * 0.65
            ia_container.content.controls[0].content.controls[2].height = page.height * 0.83 * 0.1 if ia_container.content.controls[0].height == page.height * 0.72 else page.height * 0.72 * 0.1
            ia_container.content.controls[0].height = page.height * 0.83 if ia_container.content.controls[0].height == page.height * 0.72 else page.height * 0.72
            page.update()
        send_button =IconButton(on_click=send_message,icon=Icons.SEND,bgcolor="#9796f0", width=page.width * 0.13)
        async def vertical_drag(e):
            data = json.loads(e.data)
            logger.debug(f"Swipe data: pv={data['pv']}, vy={data['vy']}")
            if data["pv"] > 1 and data["vy"] > 0:
                send_button.focus()
        ia_container = GestureDetector(
            on_tap=lambda e: send_button.focus(),
            on_vertical_drag_end=vertical_drag,
            content=Stack(controls=[
                Container(
                    height=page.height * 0.72, 
                    width=page.width, 
                    gradient=LinearGradient(
                        begin=flet.Alignment.TOP_LEFT,
                        end=flet.Alignment(0.8, 1),
                        colors=[
                            "#9796f0", # Blau pastel
                            "#fbc7d4", # Vermell pastel
                        ],
                        tile_mode=GradientTileMode.MIRROR,
                        rotation=math.pi / 3,
                    ), 
                    bottom=0, 
                    border_radius=20,
                    content=Column(
                        height=page.height * 0.72,
                        controls=[
                            Container(
                                height=page.height * 0.72 * 0.15, 
                                width=page.width,
                                bgcolor="#9796f0",
                                content=Row([
                                    IconButton(Icons.OPEN_IN_FULL_ROUNDED, icon_color="d1ddff", on_click=fullscreen),
                                    Text("NEAR IA", style=TextStyle(size=24, color="white"), text_align="center"),
                                    IconButton(Icons.CLOSE_ROUNDED, icon_color="#fbc7d4", on_click=exit_e)
                                ], alignment=MainAxisAlignment.SPACE_BETWEEN, width=page.width)
                            ),
                            ListView(
                                auto_scroll=True,
                                height=page.height * 0.72 * 0.65, 
                                controls=[]
                            ), 
                            Row(height=page.height * 0.72 * 0.1, width=page.width, vertical_alignment="end", controls=[
                                Text(""),
                                TextField(width=page.width * 0.8, label="Parla amb la IA!", autocorrect=True, icon=Icons.ACCOUNT_CIRCLE, multiline=True, on_submit=send_message),
                                send_button
                            ])
                        ]
                    )
                )
            ])
        )

        global canvi, ai, Yelp, Sostenible_L, Foursquare
        
        # Avoid duplicate views in stack
        if len(page.views) > 0 and page.views[-1].route == page.route:
            return

        if page.route != '/info':
            page.controls.clear()  
        
        if page.route == '/':
            logger.info("=== RUTA: / (Pantalla principal) ===")
            if len(cards) >= 1:
                logger.info(f"Mostrant {len(cards)} cards")
                # selected_llocs.offset = Offset(0,0)
                cards[0].scale = 1
                cards[0].opacity = 1
                botons.opacity = 1
                Tags_amunt.opacity = 1
                page.views.append(View(
                    route='/',
                    padding=0,
                    controls=[Tags_amunt_safe,stack_cards,botons],
                    navigation_bar=page.navigation_bar
                ))
            else:
                logger.warning("No hi ha cards disponibles - Redirigint a /error")
                await page.push_route("/error")
        
        if page.route == '/error':
            page.views.append(await error_view(page, size_botons, Tags_amunt_safe, update_cards, scale_next_card, config_near))

        if page.route == '/favorits':
            logger.info("Favorits seleccionat")
            page.views.append(await favorits_view(page, get_client_storage))

        if page.route == '/configuracio':
            page.views.append(View(
                route='/configuracio',
                padding=0,
                controls=[configuracio], 
                bgcolor="#FFFCF1",
                navigation_bar=page.navigation_bar
            ))
            logger.info("Configuració seleccionada")

        if page.route == '/configuracio/historial': 
            logger.info("Historial seleccionat")
            page.views.append(await historial_view(page, get_client_storage))

        if page.route == '/configuracio/tema':
            page.views.append(under_construction_view(page, title="Tema", route='/configuracio/tema'))

        if page.route == '/configuracio/politica_privacitat':
            page.views.append(under_construction_view(page, title="Política de privacitat", route='/configuracio/politica_privacitat'))

        if page.route == '/configuracio/idioma':
            async def idioma_canviat(e):
                APP_SESSIONS[page]["idioma"] = e.control.value
            
            page.views.append(idioma_view(page, APP_SESSIONS, idioma_canviat))

        if page.route == "/configuracio/config_near":
            async def event_lloc_especific(e):
                await page.push_route("/lloc_especific")
                
            page.views.append(await config_near_view(page, APP_SESSIONS, get_client_storage, event_lloc_especific))
            
            # Recuperem la variable canvi en el cas que algun valor hagi estat modificat al fitxer (desat al diccionari de la sessio temporal)
            if APP_SESSIONS[page].get("canvi"):
                global canvi
                canvi = True
                APP_SESSIONS[page]["canvi"] = False

        if page.route == '/configuracio/sobre_app':
            page.views.append(about_view(page))
        if page.route == '/info': 
            page.views.append(info_view(page))
        if page.route == '/categories':
            page.add(Tags_amunt_safe,stack_cards,botons)
            page.views.append(categories_view(page, APP_SESSIONS, view_pop, categ_check_sel))
        
        if page.route == "/configuracio/ajuda":
            page.views.append(ajuda_view(page))
        
        if page.route == "/lloc_especific":
            def lloc_especific(e):
                global canvi
                logger.debug(e.control.value)
                APP_SESSIONS[page]["lloc_especific"] = e.control.value
                canvi = True
                
            page.views.append(lloc_especific_view(page, APP_SESSIONS, lloc_especific))
        
        if page.route == "/ia":
            global ai
            ai = 2
            await ia_view_setup(page, APP_SESSIONS, ia_container, first_message)
        
        page.update()
    
    page.on_route_change = on_change_page 
    page.on_view_pop = view_pop
    
    async def seguent(e):
        cards[0].offset = Offset(-4, 0)  
        page.update()
        await asyncio.sleep(0.15)  
        cards.remove(cards[0])
        logger.debug(f"Card {len(cards)} swiped left")
        await update_cards()
        await scale_next_card()
    
    async def guarda(e):
        global index_photo_stack
        saved_cards = await get_client_storage(page).get_async("saved_cards")
        dadesLlocs = APP_SESSIONS[page].get("dadesLlocs")
        images_request = APP_SESSIONS[page].get("images_request")
        saved_cards_images = await get_client_storage(page).get_async("saved_cards_images")   
        saved_cards.append(dadesLlocs[index_photo_stack])
        saved_cards_images.append(images_request[index_photo_stack][0]) if images_request[index_photo_stack] != [] else saved_cards_images.append(images_request[index_photo_stack])
        saved_cards = await get_client_storage(page).set_async("saved_cards", saved_cards)
        saved_cards_images = await get_client_storage(page).set_async("saved_cards_images", saved_cards_images)
        cards[0].offset = Offset(4, 0)  
        page.update()
        await asyncio.sleep(0.15)  
        cards.remove(cards[0])
        logger.debug(f"Card {len(cards)} swiped left")
        await update_cards()
        await scale_next_card()

    async def mes_info(e):
        #Animació en general per fer desapareixer tot 
        cards[0].animate_scale = Animation(550)
        cards[0].scale = 2
        cards[0].opacity = 0.1
        botons.animate_opacity = Animation(550)
        Tags_amunt.animate_opacity = Animation(550)
        botons.opacity = 0.12
        Tags_amunt.opacity = 0.12
        page.update()
        await asyncio.sleep(0.5)
        page.controls.clear()
        page.update()
        #Comença a afegir l'altre pàgina
        await page.push_route('/info')

    async def categ_check_sel(e):
        global canvi
        categories_sel = APP_SESSIONS[page].get("categories_sel")
        if e.control.value == True:
            categories = CATEGORIES_LIST.get(e.control.label, [])
            for category in categories:
                if category not in categories_sel:
                    categories_sel.append(category)
                    APP_SESSIONS[page]["categories_sel"] = categories_sel
                    canvi = True
        else: 
            categories = CATEGORIES_LIST.get(e.control.label, [])
            for category in categories:
                if category in categories_sel:
                    categories_sel.remove(category)
                    APP_SESSIONS[page]["categories_sel"] = categories_sel
                    canvi = True
        categories_sel = APP_SESSIONS[page].get("categories_sel")
        logger.debug(categories_sel)
    async def categ_chip_sel(e):
        global canvi
        global ai 
        categories_sel = APP_SESSIONS[page].get("categories_sel")
        if e.control.selected:# El que fa es afegir en el cas de que estigui seleccionat i detecta la chip
            categories = CATEGORIES_LIST.get(e.control.label.value, [])
            for category in categories:
                if category not in categories_sel:
                    categories_sel.append(category)
                    APP_SESSIONS[page]["categories_sel"] = categories_sel
                    canvi = True
        else:
            categories = CATEGORIES_LIST.get(e.control.label.value, [])
            for category in categories:
                if category in categories_sel:
                    categories_sel.remove(category)
                    APP_SESSIONS[page]["categories_sel"] = categories_sel
                    canvi = True
        if e.control.label.value == "   Cerca a un lloc     ":
            await page.push_route('/lloc_especific')
            e.control.selected = False
        if e.control.label.value == "AI":
            if e.control.selected and ai != 2:
                ai = 2
                await page.push_route("/ia") 

            else:
                await page.push_route('/')
                page.overlay.clear()
                # page.overlay.append(gl)

                    
            page.update()

        
        categories_sel = APP_SESSIONS[page].get("categories_sel")
        logger.debug(categories_sel)
        
    
    async def mes_info_select(e):
        await page.push_route('/categories')
        Tags_amunt.controls[len(Tags_amunt.controls) - 1].content.selected = False


#Definirem aqui tots els components com a variables per a tal d'accedir-hi en qualsevol moment en el programa
    Tags_amunt =Row( #Totes les etiquetes juntes 
                spacing=5,
                alignment= "center",
                scale=0.952,
                controls=[
                    Container(border=Border.all(1, "#c4e4da"),border_radius=15.5,content=Chip(
                        selected_color="#6fa4a6",
                        bgcolor="#E8EEED",
                        label=Text("Restaurants",weight=FontWeight.W_400,),
                        leading=Icon(Icons.RESTAURANT_MENU_OUTLINED),
                        on_select=categ_chip_sel,
                        shadow_color = "#9ebdbf",
                        selected_shadow_color = "9ebdbf",
                        elevation=2,
                        shape = RoundedRectangleBorder(radius=14.5),
                        show_checkmark=False,
                    )), 
                    Container(border=Border.all(1, "#c4e4da"),border_radius=15.5,content=Chip(
                        selected_color="#6fa4a6",
                        bgcolor="#E8EEED",
                        label=Text("Llocs emblematics",weight=FontWeight.W_400,),
                        leading=Icon(Icons.MUSEUM_OUTLINED),
                        on_select=categ_chip_sel,
                        shadow_color = "#9ebdbf",
                        selected_shadow_color = "9ebdbf",
                        elevation=2,
                        shape = RoundedRectangleBorder(radius=14.5),
                        show_checkmark=False,
                    )), 
                    Container(border=Border.all(1, "#c4e4da"),border_radius=15.5,content=Chip(
                        selected_color="#6fa4a6",
                        bgcolor="#E8EEED",
                        label=Text("Parcs",weight=FontWeight.W_400,),
                        leading=Icon(Icons.PARK_OUTLINED),
                        on_select=categ_chip_sel,
                        shadow_color = "#9ebdbf",
                        selected_shadow_color = "9ebdbf",
                        elevation=2,
                        shape = RoundedRectangleBorder(radius=14.5),
                        show_checkmark=False,
                    )), 
                    Container(border=Border.all(1, "#c4e4da"),border_radius=15.5,content=Chip(
                        selected_color="#6fa4a6",
                        bgcolor="#E8EEED",
                        label=Text("Cafeteries",weight=FontWeight.W_400,),
                        leading=Icon(Icons.LOCAL_CAFE_OUTLINED),
                        on_select=categ_chip_sel,
                        shadow_color = "#9ebdbf",
                        selected_shadow_color = "9ebdbf",
                        elevation=2,
                        shape = RoundedRectangleBorder(radius=14.5),
                        show_checkmark=False,
                    )), 
                    Container(border=Border.all(1, "#c4e4da"),border_radius=15.5,content=Chip(
                        selected_color="#6fa4a6",
                        bgcolor="#E8EEED",
                        label=Text("Entreteniment",weight=FontWeight.W_400,),
                        leading=Icon(Icons.INSERT_EMOTICON_OUTLINED),
                        on_select=categ_chip_sel,
                        shadow_color = "#9ebdbf",
                        selected_shadow_color = "9ebdbf",
                        elevation=2,
                        shape = RoundedRectangleBorder(radius=14.5),
                        show_checkmark=False,
                    )), 
                    Container(border=Border.all(1, "#c4e4da"),border_radius=15.5,content=Chip(
                        selected_color="#6fa4a6",
                        bgcolor="#E8EEED",
                        label=Text("Botigues",weight=FontWeight.W_400,),
                        leading=Icon(Icons.SHOPPING_BAG_OUTLINED),
                        on_select=categ_chip_sel,
                        shadow_color = "#9ebdbf",
                        selected_shadow_color = "9ebdbf",
                        elevation=2,
                        shape = RoundedRectangleBorder(radius=14.5),
                        show_checkmark=False,
                    )), 
                    Container(border=Border.all(1, "#c4e4da"),border_radius=15.5,content=Chip(
                        selected_color="#6fa4a6",
                        bgcolor="#E8EEED",
                        label=Text("Turisme",weight=FontWeight.W_400,),
                        leading=Icon(Icons.FLIGHT_OUTLINED),
                        on_select=categ_chip_sel,
                        shadow_color = "#9ebdbf",
                        selected_shadow_color = "9ebdbf",
                        elevation=2,
                        shape = RoundedRectangleBorder(radius=14.5),
                        show_checkmark=False,
                    )), 
                    Container(border=Border.all(1, "#9796f0"),border_radius=15.5,content=Chip(
                        selected_color="#9796f0",
                        bgcolor="#E8EEED",
                        label=Text("AI",weight=FontWeight.W_100),
                        leading=Icon(Icons.CIRCLE, color="#C8A2C8"),
                        on_select=categ_chip_sel,
                        shadow_color = "#9796f0",
                        selected_shadow_color = "C8A2C8",
                        elevation=2,
                        shape = RoundedRectangleBorder(radius=14.5),
                        show_checkmark=False,
                    )), 
                    Container(border=Border.all(1, "#829891"),border_radius=15.5,content=Chip(
                        selected_color="#6fa4a6",
                        bgcolor="#E8EEED",
                        label=Text("Més",weight=FontWeight.W_400,),
                        leading=Icon(Icons.READ_MORE_OUTLINED,color="black"),
                        on_select=mes_info_select,
                        shadow_color = "#9ebdbf",
                        selected_shadow_color = "9ebdbf",
                        elevation=2,
                        shape = RoundedRectangleBorder(radius=14.5),
                        show_checkmark=False,
                    )), 
                ],
                scroll="hidden",
    )
    size_botons = page.width / 30
    if size_botons >= 14:
        size_botons = 14
    botons = ResponsiveRow(
        vertical_alignment="end",
        controls=[
            Container(
                col=4,
                border=Border.all(2, "#eb4d46"),
                border_radius=28,
                bgcolor="#d9acaa",
                alignment=flet.Alignment.CENTER,
                on_click=seguent,
                width=page.width / 3.2,
                height=page.height * 0.05,
                content=Icon(Icons.CLOSE, color="black", size=32),
                ink=True,
                clip_behavior="antiAlias",
            ),
            Container(
                col=4,
                border=Border.all(2, "#e6e3da"),
                border_radius=28,
                bgcolor="#FBF9F1",
                alignment=flet.Alignment.CENTER,
                on_click=mes_info,
                width=page.width / 3.2,
                height=page.height * 0.05,
                content=Icon(Icons.INFO_OUTLINE, color="black", size=32),
                ink=True,
                clip_behavior="antiAlias",
            ),
            Container(
                col=4,
                border=Border.all(2, "#7bedba"),
                border_radius=28,
                bgcolor="#aad9c4",
                alignment=flet.Alignment.CENTER,
                on_click=guarda,
                width=page.width / 3.2,
                height=page.height * 0.05,
                content=Icon(Icons.FAVORITE_BORDER, color="black", size=32),
                ink=True,
                clip_behavior="antiAlias",
            ),
        ]
    )
    stack_cards = Stack(alignment=flet.Alignment.CENTER, offset=(0,0), expand = True)
    images_saved = GridView(
        expand=True,
        height=page.height * 0.89, 
        runs_count=3,
        child_aspect_ratio=1,
        spacing=25,
        run_spacing=5
    )
    
    async def tema(e):
        await page.push_route('/configuracio/tema')
    async def Historial(e):
        await page.push_route("/configuracio/historial")
    async def Idioma(e):
        await page.push_route("/configuracio/idioma")
    async def config_near(e):
        await page.push_route("/configuracio/config_near")
    async def sobre_app(e):
        await page.push_route("/configuracio/sobre_app")
    async def ajuda(e):
        await page.push_route("/configuracio/ajuda")
    async def politica_privacitat(e):
        await page.push_route("/configuracio/politica_privacitat")

    configuracio =Card(bgcolor = "#AAD7D9", height=page.height * 0.8, expand=True,
            content=Container(
                content=Column(
                    [
                        ListTile(
                            title=Text("Configuració", theme_style=TextThemeStyle.HEADLINE_SMALL, weight=FontWeight.W_500),
                            height=(page.height * 0.8) / 13,
                        ),
                        ListTile(title=Text("General"), dense=True,height=(page.height * 0.8) / 10),
                        ListTile(
                            leading=Icon(Icons.PALETTE_OUTLINED, color="black"),
                            trailing = Icon(Icons.CHEVRON_RIGHT_OUTLINED),
                            title=Text("Tema", color="black"),
                            selected=True,
                            height=(page.height * 0.8) / 13,
                            on_click=tema
                        ),
                        ListTile(
                            leading=Icon(Icons.LANGUAGE, color="black"),
                            trailing = Icon(Icons.CHEVRON_RIGHT_OUTLINED),
                            title=Text("Idioma", color="black"),
                            selected=True,
                            height=(page.height * 0.8) / 13,
                            on_click=Idioma
                        ),
                        ListTile(
                            leading=Icon(Icons.HISTORY, color="black"),
                            trailing = Icon(Icons.CHEVRON_RIGHT_OUTLINED),
                            title=Text("Historial de llocs", color="black"),
                            selected=True,
                            height=(page.height * 0.8) / 13,
                            on_click=Historial
                        ),
                        ListTile(
                            leading=Icon(Icons.NEAR_ME_OUTLINED, color="black"),
                            trailing = Icon(Icons.CHEVRON_RIGHT_OUTLINED),
                            title=Text("Pàrametres cerca de llocs", color="black"),
                            selected=True,
                            height=(page.height * 0.8) / 13,
                            on_click=config_near
                        ),
                        ListTile(title=Text("Jo i l'App"), dense=True,height=(page.height * 0.8) / 10),
                        ListTile(
                            leading=Icon(Icons.INFO_OUTLINED, color="black"),
                            trailing = Icon(Icons.CHEVRON_RIGHT_OUTLINED),
                            title=Text("Sobre l'App", color="black"),
                            height=(page.height * 0.8) / 13,
                            selected=True,
                            on_click=sobre_app
                        ),
                        ListTile(
                            leading=Icon(Icons.PRIVACY_TIP_OUTLINED, color="black"),
                            trailing = Icon(Icons.CHEVRON_RIGHT_OUTLINED),
                            title=Text("Politica de privacitat", color="black"),
                            selected=True,
                            height=(page.height * 0.8) / 13,
                            on_click=politica_privacitat
                        ),
                        ListTile(
                            leading=Icon(Icons.HELP_OUTLINED, color="black"),
                            trailing = Icon(Icons.CHEVRON_RIGHT_OUTLINED),
                            title=Text("Ajuda", color="black"),
                            selected=True,
                            height=(page.height * 0.8) / 13,
                            on_click=ajuda
                        ),
                    ],
                    spacing=0,
                ),
            )
        )

    configuracio = SafeArea(content=configuracio)

    async def changetab(e):
        global ai
        index = e.control.selected_index

        if index == 1: #Llocs
            ai+=1
            if ai == 2:
                await page.push_route("/ia")    
                page.update()            
            elif ai == 4:
                page.overlay.clear()
                # page.overlay.append(gl)
            await page.push_route('/')
            
        elif index == 0: #Favorits
            ai=0
            page.overlay.clear()
            # page.overlay.append(gl)
            await page.push_route('/favorits')

        elif index == 2: #Configuració
            ai=0
            page.overlay.clear()
            # page.overlay.append(gl)
            await page.push_route('/configuracio')
             
        page.update()
    
    # selected_favorits =Icon(icon=Icons.FAVORITE_ROUNDED, color="#E78895", animate_size=200)
    # selected_llocs =Icon(icon=Icons.LOCATION_PIN, color=Colors.BLACK, animate_offset=140, offset=Offset(0,0)) 
    # selected_configuracio = Icon(icon=Icons.SETTINGS_ROUNDED, color=Colors.BLACK, rotate=Rotate(0, alignment=flet.Alignment.CENTER), animate_rotation=Animation(duration=1000, curve="bounceOut"))
    
    page.navigation_bar=NavigationBar(
        bgcolor = "#6fa4a6",
        selected_index = 1,
        indicator_color = "#FBF9F1",
        on_change=changetab,
        destinations=[
            NavigationBarDestination(label="Favorits", icon=Icons.FAVORITE_BORDER_ROUNDED, selected_icon=Icons.FAVORITE_ROUNDED),
            NavigationBarDestination(label="Llocs", icon=Icons.LOCATION_ON_OUTLINED, selected_icon=Icons.LOCATION_PIN), 
            NavigationBarDestination(label="Configuració", icon=Icons.SETTINGS_OUTLINED, selected_icon=Icons.SETTINGS_ROUNDED),
        ]
    )
    
    botons.height = page.height * 0.08
    botons.width = page.width
    # page.navigation_bar.height = page.height * 0.11
    Tags_amunt.height = page.height * 0.045
    Tags_amunt.width = page.width 
    stack_cards.height = page.height * 0.8
    stack_cards.width = page.width 
   
    async def on_swipe(e):
        data = json.loads(e.data)
        logger.debug(data["pv"])
        if data["pv"] != 0:
            if data["pv"] < 1: #Esquerra
                await seguent(e)
            elif data["pv"] > 0: #Dreta
                await guarda(e)

    async def on_swipe_vertical(e):
        data = json.loads(e.data)
        logger.debug(data["pv"])
        if data["pv"] < 1 and data["vy"] < 0:
            await mes_info(e)
            
    # Aquest el que fa es convertir cada card individual en GestureDetector. Amb això, podem detectar cap a on es mou i com funciona. Es molt útil i ens ho serà en un futur.
    async def update_cards():
        logger.info("=== INICI UPDATE_CARDS ===")
        stack_cards.controls.clear() 
        global index_photo_stack, images_request, canvi, cards, sostenible, sostenible_2, Yelp, Foursquare, Sostenible_L
        logger.debug(f"Variables globals - canvi: {canvi}, sostenible: {sostenible}, sostenible_2: {sostenible_2}")
        if canvi == True:
            logger.info("Canvi activat - Mostrant splash screen")
            #crearem la splash screen
            splash = Container(
                content=Lottie(src='src/NearHere.json'),
                alignment=flet.Alignment.CENTER,
                expand=True,
            )
            page.overlay.append(splash)
            page.update()
        #:) Solucionat tot emmagatzemat!!!!!!!!
        loc_visited = await get_client_storage(page).get_async("loc_visited") 
        categories_sel = APP_SESSIONS[page].get("categories_sel")
        logger.debug(f"Configuracio carregada - categories_sel: {categories_sel}")
        sort_sel = await get_client_storage(page).get_async("sort_sel")
        radius_sel = await get_client_storage(page).get_async("radius_sel")
        preu = await get_client_storage(page).get_async("preu")
        
        logger.info(f"Parametres de cerca - Sort: {sort_sel}, Categories: {categories_sel}, Radius: {radius_sel}m, Preu: {preu}")
        logger.debug(f"Llocs visitats: {len(loc_visited) if loc_visited else 0}")
        
        if len(cards) == 0 or canvi == True:
                logger.info("Iniciant proces de demanar dades - Cards buides o canvi activat")
                #* Demanem les dades 
                logger.debug(f"index_photo_Stack: {index_photo_stack}")
                if canvi == True:
                    sostenible = True
                    sostenible_2 = True
                    logger.info(f"Reset variables - sostenible: {sostenible}, sostenible_2: {sostenible_2}")
                    logger.info(f"Llocs visitats abans del reset: {len(loc_visited)}")
                    dadesLlocs = []
                    cards.clear()

                index_photo_stack = -1
                #:) Cobren el mateix demanant 5, 10 que 50º
                dadesLlocs = APP_SESSIONS[page].get("dadesLlocs")
                p = await gl.get_current_position()
                logger.info(f"Posicio actual obtinguda: Lat={p.latitude}, Long={p.longitude}")
                
                # Respecta la preferència de font de dades amb alternatives
                data_source_pref = await get_client_storage(page).get_async("data_source_pref") or "AUTO"

                def ordre_per_preferencia(pref):
                    if pref == "SOSTENIBLE":
                        return ["SOSTENIBLE", "YELP", "FOURSQUARE"]
                    if pref == "YELP":
                        return ["YELP", "FOURSQUARE", "SOSTENIBLE"]
                    if pref == "FOURSQUARE":
                        return ["FOURSQUARE", "YELP", "SOSTENIBLE"]
                    return ["SOSTENIBLE", "YELP", "FOURSQUARE"]  # AUTO

                Foursquare, Yelp, Sostenible_L = False, False, False
                dadesLlocs = "error 400"
                llocs = None

                ordre = ordre_per_preferencia(data_source_pref)

                for origen in ordre:
                    if origen == "SOSTENIBLE":
                        logger.info("Intent: Cercant llocs sostenibles")
                        Foursquare, Yelp, Sostenible_L = False, False, True
                        if "lloc_especific" in APP_SESSIONS[page]:
                            lloc_especific = APP_SESSIONS[page].get("lloc_especific")
                            if lloc_especific != "":
                                logger.warning("Llocs sostenibles no suporten cerca per lloc especific - Saltant a següent font")
                                dadesLlocs = "error 400"
                            else:
                                llocs = LLocs_sostenibles(p.latitude,p.longitude,radius_sel,50,loc_visited,categories_sel)
                                dadesLlocs, loc_visited = llocs.dades()
                        else:
                            llocs = LLocs_sostenibles(p.latitude,p.longitude,radius_sel,50,loc_visited,categories_sel)
                            dadesLlocs, loc_visited = llocs.dades()
                        logger.debug(f"Resultat llocs sostenibles: {type(dadesLlocs)}, {len(dadesLlocs) if isinstance(dadesLlocs, list) else dadesLlocs}")
                    elif origen == "YELP":
                        logger.info("Intent: Cercant llocs amb Yelp API")
                        Foursquare, Yelp, Sostenible_L = False, True, False
                        if "lloc_especific" in APP_SESSIONS[page]:
                            lloc_especific = APP_SESSIONS[page].get("lloc_especific")
                            if lloc_especific != "":
                                llocs = Llocs_yelp(None,None,radius_sel,2,loc_visited,categories_sel,sort_sel, preu, lloc_especific)
                                dadesLlocs, loc_visited = llocs.dades()
                            else:
                                llocs = Llocs_yelp(p.latitude,p.longitude,radius_sel,50,loc_visited,categories_sel,sort_sel, preu, None)
                                dadesLlocs, loc_visited = llocs.dades()
                        else:
                            llocs = Llocs_yelp(p.latitude,p.longitude,radius_sel,50,loc_visited,categories_sel,sort_sel, preu, None)
                            dadesLlocs, loc_visited = llocs.dades()
                        logger.debug(f"Resultat Yelp: {type(dadesLlocs)}, {len(dadesLlocs) if isinstance(dadesLlocs, list) else dadesLlocs}")
                    elif origen == "FOURSQUARE":
                        logger.info("Intent: Cercant llocs amb Foursquare API")
                        Foursquare, Yelp, Sostenible_L = True, False, False
                        if "lloc_especific" in APP_SESSIONS[page]:
                            lloc_especific = APP_SESSIONS[page].get("lloc_especific")
                            if lloc_especific != "":
                                llocs = Llocs(None,None,radius_sel,50,loc_visited,categories_sel,sort_sel, preu, lloc_especific)
                                dadesLlocs, loc_visited = llocs.dades()
                            else:
                                llocs = Llocs(p.latitude,p.longitude,radius_sel,50,loc_visited,categories_sel,sort_sel, preu, None)
                                dadesLlocs, loc_visited = llocs.dades()
                        else:
                            llocs = Llocs(p.latitude,p.longitude,radius_sel,50,loc_visited,categories_sel,sort_sel, preu, None)
                            dadesLlocs, loc_visited = llocs.dades()
                        logger.debug(f"Resultat Foursquare: {type(dadesLlocs)}, {len(dadesLlocs) if isinstance(dadesLlocs, list) else dadesLlocs}")

                    # Si hem obtingut una llista vàlida, parem de provar fonts
                    if isinstance(dadesLlocs, list):
                        break

                # Reset flags heretats de l'estratègia anterior
                sostenible_2 = False
                sostenible = False
                #dadesLlocs, loc_visited = llocs.dades()
                logger.info(f"Verificant resultats finals - Tipus: {type(dadesLlocs)}, Es llista: {isinstance(dadesLlocs, list)}")
                if dadesLlocs == "error 400" or dadesLlocs == "error 400 de l'API sostenible" or not isinstance(dadesLlocs, list):
                    logger.error(f"ERROR FINAL: Cap API ha retornat resultats valids - dadesLlocs: {dadesLlocs}")
                    await page.push_route("/error")
                else:
                    logger.info(f"EXIT: Llocs trobats: {len(dadesLlocs)} - Origen: {'Sostenible' if Sostenible_L else 'Yelp' if Yelp else 'Foursquare'}")
                    APP_SESSIONS[page]["dadesLlocs"] = dadesLlocs
                    if dadesLlocs == []:
                        logger.warning("Llista de llocs buida - Redirigint a pagina d'error")
                        await page.push_route("/error")
                    images_request = llocs.photos()
                    APP_SESSIONS[page]["images_request"] = images_request
                    logger.debug(f"Imatges sol·licitades: {len(images_request)}")
                    categories = llocs.categories()
                    categories_visited = await get_client_storage(page).get_async("categories_visited")
                    categories_visited.extend(categories)
                    await get_client_storage(page).set_async("categories_visited", categories_visited)
                    # print(categories)
                    def distancia(i): #La fórmula de Haversine
                        latitude_inicial = math.radians(p.latitude)
                        longitude_inicial = math.radians(p.longitude)
                        latitude_final = math.radians(dadesLlocs[i]['geocodes']['main']['latitude'])
                        longitude_final = math.radians(dadesLlocs[i]['geocodes']['main']['longitude'])
                        # Ara després de passar a radians el que fem és fer la diferencia entre latituds i longituds.
                        dif_1 = latitude_final  - latitude_inicial
                        dif_2 = longitude_final  - longitude_inicial
                        #Apliquem la formula ara 
                        a = math.sin(dif_1/2)**2 + math.cos(latitude_inicial) * math.cos(latitude_final) * math.sin(dif_2/2)**2
                        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
                        R = 6371000 # I multipliquem pel radi de la terra
                        d = R * c
                        if d > 1000:
                            return f"{round(d/1000)} Km"
                        else:
                            return f"{round(d)} m"
                    
                    # Verificació de seguretat: assegurem que dadesLlocs és una llista vàlida
                    if not isinstance(dadesLlocs, list) or dadesLlocs == "error 400":
                        logger.error(f"ERROR CRITIC: dadesLlocs no es una llista valida - Tipus: {type(dadesLlocs)}, Valor: {dadesLlocs}")
                        await page.push_route("/error")
                        return
                    
                    logger.info(f"Iniciant creacio de {len(dadesLlocs)} cards")
                    for i in range(len(dadesLlocs)):
                        logger.debug(f"Processant card {i+1}/{len(dadesLlocs)} - Tipus dada: {type(dadesLlocs[i])}")
                        # Definim tots els components de la card
                        if not isinstance(dadesLlocs[i], dict):
                            logger.error(f"ERROR: dadesLlocs[{i}] no es un diccionari - Tipus: {type(dadesLlocs[i])}, Valor: {dadesLlocs[i]}")
                            continue
                        
                        logger.debug(f"Card {i}: {dadesLlocs[i].get('name', 'Nom desconegut')}")
                        if 'address' in dadesLlocs[i]["location"]: 
                            subtitle_card = Column(horizontal_alignment="center", controls=[
                                Text(f"Direcció: {dadesLlocs[i]['location']['address']} | Distància: {distancia(i)}", color="white", weight=FontWeight.W_900),
                                Row(alignment="center",width = page.width, controls=[])
                                ]) 
                        else: 
                            subtitle_card = Column(horizontal_alignment="center", controls=[
                                Text(f"Direcció: {None} | Distància: {distancia(i)}", color="white",weight=FontWeight.W_900),
                                Row(alignment="center",width = page.width, controls=[])
                                ]) 
                        if categories[i] != []:
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
                        min_size = base_size - 25
                        max_size = base_size - 13
                        async def imatge_en_gran(e):
                            img_principal = stack_cards.controls[0].content.content.controls[1].content.controls[0].content.content 
                            dlg = AlertDialog(
                                bgcolor=Colors.with_opacity(0, '#ff6666'),

                                content=InteractiveViewer(
                                    min_scale=0.1,
                                    max_scale=15,
                                    boundary_margin=Margin.all(20),
                                    content=Image(src=img_principal.src)
                                )
                            )
                            page.open(dlg)
                        # Adjust size_title based on the length of dadesLlocs[i]["name"]
                        size_title = get_dynamic_font_size(dadesLlocs[i]["name"], base_size, min_size, max_size) # :) Mig solucionat
                        #size_title = (page.height * 0.055) - 10 #! BUG-7
                        nom_del_restaurant = Stack(
                                alignment=flet.Alignment.CENTER,
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
                                        alignment=flet.Alignment.CENTER
                                    ),
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
                                                        size=size_title,
                                                        weight=FontWeight.W_900,
                                                        font_family="WorkSans",
                                                        color=Colors.BLACK,
                                                    ),
                                                ),
                                            ],
                                        ),
                                        alignment=flet.Alignment.CENTER
                                    ),
                                ],
                            )
    
                        logger.debug(f"images_request i {images_request[i]}")
                        logger.debug(f"index_photo_stack {index_photo_stack}")

                        async def check_image_url(url):
                            # Skip check for URLs we know are good
                            if url and (url.startswith("https://fastly.4sqi.net") or 
                                      url.startswith("https://s3-media") or
                                      url.startswith("https://static.openstreetmap.org")):
                                return True
                            
                            # Only check other URLs
                            async with httpx.AsyncClient() as client:
                                try:
                                    response = await client.head(url, timeout=2.0) # Add timeout
                                    return response.status_code == 200
                                except:
                                    return False

                        img_principal = Container(
                            alignment=flet.Alignment.CENTER,
                            on_click=imatge_en_gran,
                            content=InteractiveViewer(
                                min_scale=0.1,
                                max_scale=15,
                                content=Image(
                                    animate_opacity=150, 
                                    border_radius=15,
                                    # Use asyncio.run to run the async check in sync context
                                    src=images_request[i][0] if len(images_request[i]) >= 1 and await check_image_url(images_request[i][0]) else None,
                                    width=page.width * 0.8, 
                                    height=page.height * 0.8 * 0.65, 
                                    fit="COVER"
                                )
                            )
                        )
                        img_esq =Image(
                                animate_opacity=150,
                                left=-page.width * 0.75,
                                top=33,                                     
                                src=images_request[i][len(images_request[i]) - 1] if len(images_request[i]) > 1 and requests.get(images_request[i][len(images_request[i]) - 1]).status_code == 200 else None ,#URL imatge
                                border_radius=20,
                                width = page.width * 0.8, 
                                height = page.height * 0.8 * 0.5, 
                                fit="COVER"
                            )
                        img_dret = Image(
                                animate_opacity=150,
                                right=-page.width * 0.75,
                                top=33,
                                src=images_request[i][1] if len(images_request[i]) > 1  and requests.get(images_request[i][1]).status_code == 200 else None,#URL imatge
                                border_radius=15,
                                width = page.width * 0.8, 
                                height = page.height * 0.8 * 0.5, 
                                fit="COVER"
                                )
    
                        
                        async def esq(e): #Detecta que has fet click a l'esquerra 
                            global index_photo
                            img_principal = stack_cards.controls[0].content.content.controls[1].content.controls[0].content.content
                            img_dret = stack_cards.controls[0].content.content.controls[1].content.controls[2]
                            img_esq = stack_cards.controls[0].content.content.controls[1].content.controls[1]
                            if index_photo <= 0:
                                    index_photo = len(images_request[index_photo_stack]) - 1 # Fa que sempre l'index sigui un número a dins de la llista i resta un, fent així que puguem navegar
                            else:
                                index_photo -= 1
                            img_principal.opacity = 0.1 #Animació d'opactiat, perquè l'usuari tingui més comoditat visual 
                            img_principal.update()
                            await asyncio.sleep(0.15) 
                            img_principal.src = images_request[index_photo_stack][index_photo] #Actualitza les fotos 
                            img_principal.opacity = 1
                            #Resta un en el cas que sigui a dins de la llista, sinó posa el més gran (len) - 1, ja que contem des de 0
                            img_esq.src = images_request[index_photo_stack][index_photo-1 if index_photo-1 >= 0 else (len(images_request[index_photo_stack])-1)]  
                            #Incís: Mai entendre perquè els programadors contem des de 0, i després quan fas la longitud d'una llista conta des de 1, en fi.
                            img_dret.src = images_request[index_photo_stack][index_photo+1 if index_photo+1 <= (len(images_request[index_photo_stack])- 1) else 0] 
                            #El mateix, detecta que sigui a dins de la llista i no sigui negatiu, en el cas posa 0
                            page.update()
                        async def dret(e): #Mateixos comentaris pero al reves
                            global index_photo
                            img_principal = stack_cards.controls[0].content.content.controls[1].content.controls[0].content.content
                            img_dret = stack_cards.controls[0].content.content.controls[1].content.controls[2]
                            img_esq = stack_cards.controls[0].content.content.controls[1].content.controls[1]
                            if index_photo >= (len(images_request[index_photo_stack])- 1):
                                index_photo = 0
                            else:
                                index_photo += 1
                            img_principal.opacity = 0.1 #Animació d'opactiat, perquè l'usuari tingui més comoditat visual 
                            img_principal.update()
                            await asyncio.sleep(0.15) 
                            img_principal.src = images_request[index_photo_stack][index_photo] 
                            img_principal.opacity = 1
                            img_esq.src = images_request[index_photo_stack][index_photo-1 if index_photo-1 >= 0 else (len(images_request[index_photo_stack])-1)]  
                            img_dret.src = images_request[index_photo_stack][index_photo+1 if index_photo+1 <= (len(images_request[index_photo_stack])- 1) else 0]  
                            page.update()
                        
                        logger.debug("Carta creada")
                        carta = Container(
                                image=DecorationImage(
                                    src="src/fons.jpg",
                                    fit="FILL"
                                ),
                                blur=50,
                                shadow=BoxShadow(
                                    blur_radius=4.5,
                                    color=Colors.BLACK
                                ),
                                offset=(0,0),
                                border_radius=15, 
                                width = page.width,
                                height = page.height * 0.8,
                                animate_offset=Animation(500),
                                animate_opacity = Animation(600),
                                scale=0,
                                animate_scale=Animation(340, "easeOutSine"),
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
                                                                        icon=Icons.CHEVRON_RIGHT,
                                                                        icon_color = "black",
                                                                        bgcolor="#FBF9F1",
                                                                        on_click=lambda e: asyncio.run(esq(e)),
                                                                        alignment=flet.Alignment.CENTER,
                                                                        right=2,
                                                                        width = page.window.width * 0.1,
                                                                        top=page.window.height * 0.8 * 0.7 / 2,
                                                                ),
                                                                IconButton(
                                                                        icon=Icons.CHEVRON_LEFT,
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
                        
                        if 'rating' in dadesLlocs[i]: 
                            bottom_rating = Text(f"Valoració: {dadesLlocs[i]['rating']}", color="white", weight=FontWeight.W_900)
                            carta.content.controls[2].controls.append(bottom_rating)
                        if dadesLlocs[i].get('price') is not None: 
                            bottom_price = Row([Text(f"Preu:",color="white",weight=FontWeight.W_900)])
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
                                    Icon(Icons.ATTACH_MONEY, color=color)
                                )  
                            carta.content.controls[2].controls.append(bottom_price)

                page.update()   
        if canvi == True:
            canvi = False
            page.overlay.remove(splash)
            page.update()
        first_card_added = False

        for card in cards:
            if not first_card_added:
                logger.debug("Carta insertada")
                index_photo_stack += 1
                logger.debug(f"index_photo_stack {index_photo_stack}")
                stack_cards.controls.append(
                    GestureDetector(
                        content=card,
                        on_horizontal_drag_end=on_swipe,
                        on_vertical_drag_end=on_swipe_vertical
                    )
                ) 
                # :) Solucionat!
                img_principal = stack_cards.controls[0].content.content.controls[1].content.controls[0].content.content     
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
                loc_visited = await get_client_storage(page).get_async("loc_visited")
                loc_visited_photos = await get_client_storage(page).get_async("loc_visited_photos")
                dadesLlocs = APP_SESSIONS[page].get("dadesLlocs")
                loc_visited.append(dadesLlocs[index_photo_stack])
                loc_visited_photos.append(images_request[index_photo_stack])
                await get_client_storage(page).set_async("loc_visited", loc_visited)
                await get_client_storage(page).set_async("loc_visited_photos", loc_visited_photos)

                if len(images_request[index_photo_stack]) > 1:
                    img_principal.src = images_request[index_photo_stack][0]
                    img_dret.src = images_request[index_photo_stack][1] 
                    img_esq.src = images_request[index_photo_stack][len(images_request[index_photo_stack]) - 1]
                    page.update()
                elif len(images_request[index_photo_stack]) == 1:
                    logger.debug("es 1")
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

    logger.info("Cridant update_cards() per primera vegada...")
    await update_cards()
    logger.info("update_cards() completat")
    
    #L'iniciem només començar el programa per tal de fer apareixer tots els elements i escalem la primera a 1 per tal de mostrar-la

    # Tags_amunt_safe = SafeArea(content=Tags_amunt)
    # page.add(
    #     Tags_amunt_safe,
    #     stack_cards,
    #     botons, 
    # )
    await page.push_route("/")
    page.overlay.remove(splash)
    page.update()
    await scale_next_card()
    
if __name__ == "__main__":
    flet.app(target=main, assets_dir="assets")