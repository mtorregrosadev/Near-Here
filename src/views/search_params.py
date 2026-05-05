import logging
from flet import (
    Page, View, Container, ListView, Divider, Text, Slider, Dropdown, dropdown, ElevatedButton, FontWeight, AppBar
)

logger = logging.getLogger('NearHere')

async def config_near_view(page: Page, APP_SESSIONS, get_client_storage, event_lloc_especific_callback):
    """
    Construeix la vista dels paràmetres de cerca ('/configuracio/config_near')
    """
    async def radius(e):
        # A main.py farem un setter del global canvi
        APP_SESSIONS[page]["canvi"] = True
        await get_client_storage(page).set_async("radius_sel", round(e.control.value) * 1000)

    async def sort(e):
        APP_SESSIONS[page]["canvi"] = True
        val = e.control.value
        if val == "Valoració":
            await get_client_storage(page).set_async("sort_sel", "RATING")
        elif val == "Rellevancia (default)":
            await get_client_storage(page).set_async("sort_sel", "RELEVANCE")
        elif val == "Distància":
            await get_client_storage(page).set_async("sort_sel", "DISTANCE")
        elif val == "Popularitat":
            await get_client_storage(page).set_async("sort_sel", "POPULARITY")

    async def preu_sel(e):
        APP_SESSIONS[page]["canvi"] = True
        await get_client_storage(page).set_async("preu", round(e.control.value))

    async def data_source_change(e):
        label = e.control.value
        mapping = {
            "Automàtic (recomanat)": "AUTO",
            "Sostenibles": "SOSTENIBLE",
            "Yelp": "YELP",
            "Foursquare": "FOURSQUARE",
        }
        await get_client_storage(page).set_async("data_source_pref", mapping.get(label, "AUTO"))

    # Carrega els valors actuals
    sort_sel = await get_client_storage(page).get_async("sort_sel")
    value_em = "Rellevancia (default)"
    if sort_sel == "RATING":
        value_em = "Valoració"
    elif sort_sel == "DISTANCE":
        value_em = "Distància"
    elif sort_sel == "POPULARITY":
        value_em = "Popularitat"

    radius_sel = await get_client_storage(page).get_async("radius_sel")
    if radius_sel is None:
        radius_sel = 1000
    
    preu = await get_client_storage(page).get_async("preu")
    if preu is None:
        preu = 0

    data_source_pref = await get_client_storage(page).get_async("data_source_pref")
    if data_source_pref is None:
        data_source_pref = "AUTO"
        await get_client_storage(page).set_async("data_source_pref", data_source_pref)
    
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
                Text("Configura la distància màxima la qual vols que cerqui l'algorisme!", weight=FontWeight.W_300),
                Slider(min=1, max=10, divisions=10, label="{value} Km", value=int(radius_sel/1000), on_change_end=radius, active_color="#7A9A9C", inactive_color="#c9d6d7"),
                Divider(), 
                Text("RELLEVÀNCIA, ORDRE", weight=FontWeight.W_600, size=18),
                Text("Quins llocs t'apareixeran primer?", weight=FontWeight.W_300),
                Dropdown(
                    hint_text="Pica la teva preferencia",
                    width=page.width,
                    on_select=sort,
                    value=value_em,
                    options=[
                        dropdown.Option("Rellevancia (default)"),
                        dropdown.Option("Valoració"),
                        dropdown.Option("Distància"),
                        dropdown.Option("Popularitat")
                    ]
                ),
                Divider(),
                Text("FONT DE DADES", weight=FontWeight.W_600, size=18),
                Text("Selecciona la font de dades preferida. Mantindrem els canvis i farem servir altres fonts si cal.", weight=FontWeight.W_300),
                Dropdown(
                    hint_text="Tria la font preferida",
                    width=page.width,
                    on_select=data_source_change,
                    value=data_source_label,
                    options=[
                        dropdown.Option("Automàtic (recomanat)"),
                        dropdown.Option("Sostenibles"),
                        dropdown.Option("Yelp"),
                        dropdown.Option("Foursquare")
                    ],
                ),
                Divider(),
                Text("PREU", weight=FontWeight.W_600, size=18),
                Text("Configura el preu màxim que vols pagar de l'1 al 4! 1 (barat), 4 (car). Si selecciones 0, no hi haura filtre i sortiran tots", weight=FontWeight.W_300),
                Slider(min=0, max=4, divisions=4, label="{value}", on_change_end=preu_sel, active_color="#7A9A9C", inactive_color="#c9d6d7", value=preu),
                Divider(),
                Text("Lloc específic", weight=FontWeight.W_600, size=18),
                Text("Vols cercar a un lloc el qual no sigui el teu? Fes click per seleccionar-lo!", weight=FontWeight.W_300), 
                ElevatedButton("Cercar a...", on_click=event_lloc_especific_callback, width=page.width, bgcolor="#c9d6d7", color="black")
            ],
        ),
    )

    return View(
        route='/configuracio/config_near', 
        padding=0, 
        bgcolor="#FFFCF1",
        controls=[
            AppBar(title=Text("Paràmetres de cerca"), adaptive=True, bgcolor="#AAD7D9"),
            Container(expand=True, content=parametres_cerca)
        ]
    )
