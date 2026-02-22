"""Pàgina principal: / (stack de cards)"""
from flet import SafeArea, View


async def build_view(page, ctx):
    ctx.logger.info("=== RUTA: / (Pantalla principal) ===")
    Tags_amunt_safe = SafeArea(content=ctx.Tags_amunt)

    if len(ctx.cards) >= 1:
        ctx.logger.info(f"Mostrant {len(ctx.cards)} cards")
        ctx.cards[0].scale = 1
        ctx.cards[0].opacity = 1
        ctx.botons.opacity = 1
        ctx.Tags_amunt.opacity = 1
        page.views.append(View(
            route='/',
            padding=0,
            controls=[Tags_amunt_safe, ctx.stack_cards, ctx.botons],
            navigation_bar=page.navigation_bar,
        ))
    else:
        ctx.logger.warning("No hi ha cards disponibles - Redirigint a /error")
        await page.push_route("/error")
