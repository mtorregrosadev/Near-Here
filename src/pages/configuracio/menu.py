"""Menú de configuració principal: /configuracio"""
from flet import SafeArea, View


async def build_view(page, ctx):
    ctx.logger.info("Configuració seleccionada")
    page.views.append(View(
        route='/configuracio',
        padding=0,
        controls=[ctx.configuracio],
        bgcolor="#FFFCF1",
        navigation_bar=page.navigation_bar,
    ))
