"""Selecció d'idioma: /configuracio/idioma"""
from flet import AppBar, Column, Radio, RadioGroup, SafeArea, Text, View


async def build_view(page, ctx):
    async def idioma_canviat(e):
        ctx.APP_SESSIONS[page]["idioma"] = e.control.value

    idioma = ctx.APP_SESSIONS[page].get("idioma", "")

    page.views.append(View(
        route='/configuracio/idioma',
        padding=0,
        bgcolor="#FFFCF1",
        controls=[
            AppBar(title=Text("Idioma"), adaptive=True, bgcolor="#AAD7D9"),
            SafeArea(content=Text(
                "Recorda que l'idioma de moment es només de la IA! "
                "No canvia l'idioma de l'app!!",
                width=page.width,
                text_align="center",
            )),
            RadioGroup(
                content=Column([
                    Radio(value="Català", label="Català"),
                    Radio(value="Castellano", label="Castellano"),
                    Radio(value="English", label="English"),
                ]),
                on_change=idioma_canviat,
                value=f"{idioma}" if idioma else "",
            ),
        ],
    ))
