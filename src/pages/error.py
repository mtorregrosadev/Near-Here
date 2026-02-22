"""Pàgina d'error: /error"""
import asyncio
from flet import (
    Column, Divider, ElevatedButton, FontWeight, Icon, Icons,
    Row, SafeArea, Text, TextThemeStyle, View,
)
from flet_lottie import Lottie


async def build_view(page, ctx):
    ctx.logger.info("=== RUTA: /error (Pagina d'error) ===")
    Tags_amunt_safe = SafeArea(content=ctx.Tags_amunt)

    async def refresca(e):
        ctx.logger.info("Boto refresca premut - Actualitzant cards")
        await ctx.update_cards()
        await page.push_route("/")
        await asyncio.sleep(0.01)
        await ctx.scale_next_card()

    not_found = Column([
        Text(
            "No hem trobat més llocs 😕",
            text_align="center",
            weight=FontWeight.W_900,
            theme_style=TextThemeStyle.TITLE_LARGE,
            width=page.width,
            color="#6b9e9f",
        ),
        Lottie(src="src/no_hem_trobat.json"),
        Divider(),
        Text(
            "Has seleccionat una categoria que no està disponible a la teva zona "
            "o no hem pogut trobar llocs a la teva zona o on has especificat!\n\n"
            "Prova de canviar els km de distància, o cercar en un altre lloc "
            "específic i fes clic a refrescar la pàgina!"
        ),
    ], height=page.height * 0.55)

    botons_not_found = Row(
        vertical_alignment="end",
        width=page.width,
        alignment="center",
        height=page.height * 0.15,
        controls=[
            ElevatedButton(
                content=Row([
                    Icon(Icons.SETTINGS_OUTLINED),
                    Text("Obre la configuració", size=ctx.size_botons,
                         theme_style=TextThemeStyle.LABEL_LARGE),
                ]),
                on_click=ctx.config_nav,
                bgcolor="#b2ccc6",
                color="black",
            ),
            ElevatedButton(
                content=Row([
                    Icon(Icons.AUTORENEW_OUTLINED),
                    Text("Refresca", size=ctx.size_botons,
                         theme_style=TextThemeStyle.LABEL_LARGE),
                ]),
                on_click=refresca,
                bgcolor="#b2ccc6",
                color="black",
            ),
        ],
    )

    page.views.append(View(
        route='/error',
        padding=0,
        controls=[Tags_amunt_safe, not_found, botons_not_found],
        bgcolor="#FFFCF1",
        navigation_bar=page.navigation_bar,
    ))
