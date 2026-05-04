import logging
import asyncio

from flet import (
    Page,
    View,
    Column,
    Row,
    Text,
    ElevatedButton,
    Icon,
    Icons,
    Divider,
    FontWeight,
    TextThemeStyle,
)
from flet_lottie import Lottie

logger = logging.getLogger('NearHere')

async def error_view(page: Page, size_botons, Tags_amunt_safe, update_cards, scale_next_card, config_near):
    logger.info("=== RUTA: /error (Pagina d'error) ===")
        
    async def refresca(e):
        logger.info("Boto refresca premut - Actualitzant cards")
        await update_cards()
        await page.push_route("/")
        await asyncio.sleep(0.01)
        await scale_next_card()
    
    not_found=Column([
            Text("No hem trobat més llocs 😕", text_align="center", weight=FontWeight.W_900, theme_style=TextThemeStyle.TITLE_LARGE, width=page.width, color="#6b9e9f"),
            Lottie(src="src/no_hem_trobat.json"),
            Divider(),
            Text("Has seleccionat una categoria que no està disponible a la teva zona o no hem pogut trobar llocs a la teva zona o on has especificat!\n\nProva de canviar els km de distància, o cercar en un altre lloc específic i fes clic a refrescar la pàgina!")

    ], height=page.height*0.55)
    botons_not_found = Row( #Aqui van tots els botons junts 
            vertical_alignment="end", width=page.width, alignment="center", height=page.height*0.15,
            controls=[
                ElevatedButton(content=Row([Icon(Icons.SETTINGS_OUTLINED),Text("Obre la configuració",size=size_botons,theme_style=TextThemeStyle.LABEL_LARGE)]),on_click=config_near,bgcolor="#b2ccc6",color="black"),
                ElevatedButton(content=Row([Icon(Icons.AUTORENEW_OUTLINED),Text("Refresca",size=size_botons,theme_style=TextThemeStyle.LABEL_LARGE)]),on_click=refresca,bgcolor="#b2ccc6",color="black")
    ])

    return View(
        route='/error',
        padding=0,
        controls=[Tags_amunt_safe,not_found,botons_not_found],
        bgcolor="#FFFCF1",
        navigation_bar=page.navigation_bar
    )
