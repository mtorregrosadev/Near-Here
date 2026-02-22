"""Paràmetres de cerca: /configuracio/config_near"""
import flet
from flet import (
    AppBar, Container, Divider, Dropdown, ElevatedButton, FontWeight,
    ListView, Slider, Text, TextThemeStyle, View,
)


async def build_view(page, ctx):
    async def radius(e):
        await ctx.get_client_storage(page).set_async("radius_sel", round(e.control.value) * 1000)
        radius_sel = await ctx.get_client_storage(page).get_async("radius_sel")
        ctx.logger.debug(radius_sel)
        ctx.canvi = True

    async def sort(e):
        ctx.logger.debug(e.control.value)
        mapping = {
            "Valoració": "RATING",
            "Rellevancia (default)": "RELEVANCE",
            "Distància": "DISTANCE",
            "Popularitat": "POPULARITY",
        }
        await ctx.get_client_storage(page).set_async("sort_sel", mapping.get(e.control.value, "RELEVANCE"))
        ctx.logger.debug(await ctx.get_client_storage(page).get_async("sort_sel"))
        ctx.canvi = True

    async def preu_sel(e):
        await ctx.get_client_storage(page).set_async("preu", round(e.control.value))
        ctx.logger.debug(await ctx.get_client_storage(page).get_async("preu"))
        ctx.canvi = True

    async def event_lloc_especific(e):
        await page.push_route("/lloc_especific")

    async def data_source_change(e):
        mapping = {
            "Automàtic (recomanat)": "AUTO",
            "Sostenibles": "SOSTENIBLE",
            "Yelp": "YELP",
            "Foursquare": "FOURSQUARE",
        }
        await ctx.get_client_storage(page).set_async(
            "data_source_pref", mapping.get(e.control.value, "AUTO")
        )

    sort_sel = await ctx.get_client_storage(page).get_async("sort_sel")
    value_em = {
        "RATING": "Valoració",
        "RELEVANCE": "Rellevancia (default)",
        "DISTANCE": "Distància",
        "POPULARITY": "Popularitat",
    }.get(sort_sel, "Rellevancia (default)")

    radius_sel = await ctx.get_client_storage(page).get_async("radius_sel")
    ctx.logger.debug(f"radius_sel: {radius_sel}")
    preu = await ctx.get_client_storage(page).get_async("preu")
    ctx.logger.debug(f"preu: {preu}")

    data_source_pref = await ctx.get_client_storage(page).get_async("data_source_pref")
    if data_source_pref is None:
        data_source_pref = "AUTO"
        await ctx.get_client_storage(page).set_async("data_source_pref", data_source_pref)
    data_source_label = {
        "AUTO": "Automàtic (recomanat)",
        "SOSTENIBLE": "Sostenibles",
        "YELP": "Yelp",
        "FOURSQUARE": "Foursquare",
    }.get(data_source_pref, "Automàtic (recomanat)")

    parametres_cerca = Container(
        expand=True,
        content=ListView(
            expand=True,
            controls=[
                Divider(),
                Text("RADI, DISTÀNCIA", weight=FontWeight.W_600, size=18),
                Text("Configura la distància màxima la qual vols que cerqui l'algorisme!",
                     weight=FontWeight.W_300),
                Slider(min=1, max=10, divisions=10, label="{value} Km",
                       value=int(radius_sel / 1000), on_change_end=radius,
                       active_color="#7A9A9C", inactive_color="#c9d6d7"),
                Divider(),
                Text("RELLEVÀNCIA, ORDRE", weight=FontWeight.W_600, size=18),
                Text("Quins llocs t'apareixeran primer?", weight=FontWeight.W_300),
                Dropdown(
                    hint_text="Pica la teva preferencia",
                    width=page.width,
                    on_select=sort,
                    value=value_em,
                    options=[
                        flet.dropdown.Option("Rellevancia (default)"),
                        flet.dropdown.Option("Valoració"),
                        flet.dropdown.Option("Distància"),
                        flet.dropdown.Option("Popularitat"),
                    ],
                ),
                Divider(),
                Text("FONT DE DADES", weight=FontWeight.W_600, size=18),
                Text("Selecciona la font de dades preferida. Mantindrem els canvis "
                     "i farem servir altres fonts si cal.", weight=FontWeight.W_300),
                Dropdown(
                    hint_text="Tria la font preferida",
                    width=page.width,
                    on_select=data_source_change,
                    value=data_source_label,
                    options=[
                        flet.dropdown.Option("Automàtic (recomanat)"),
                        flet.dropdown.Option("Sostenibles"),
                        flet.dropdown.Option("Yelp"),
                        flet.dropdown.Option("Foursquare"),
                    ],
                ),
                Divider(),
                Text("PREU", weight=FontWeight.W_600, size=18),
                Text("Configura el preu màxim que vols pagar de l'1 al 4! "
                     "1 (barat), 4 (car). Si selecciones 0, no hi haura filtre i sortiran tots",
                     weight=FontWeight.W_300),
                Slider(min=0, max=4, divisions=4, label="{value}",
                       on_change_end=preu_sel, active_color="#7A9A9C",
                       inactive_color="#c9d6d7", value=preu),
                Divider(),
                Text("Lloc específic", weight=FontWeight.W_600, size=18),
                Text("Vols cercar a un lloc el qual no sigui el teu? "
                     "Fes click per seleccionar-lo!", weight=FontWeight.W_300),
                ElevatedButton("Cercar a...", on_click=event_lloc_especific,
                               width=page.width, bgcolor="#c9d6d7", color="black"),
            ],
        ),
    )

    page.views.append(View(
        route='/configuracio/config_near',
        padding=0,
        bgcolor="#FFFCF1",
        controls=[
            AppBar(title=Text("Paràmetres de cerca"), adaptive=True, bgcolor="#AAD7D9"),
            Container(expand=True, content=parametres_cerca),
        ],
    ))
