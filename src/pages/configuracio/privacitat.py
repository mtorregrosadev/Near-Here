"""Política de privacitat: /configuracio/politica_privacitat"""
from flet import (
    AppBar, Column, Divider, FontWeight, MainAxisAlignment,
    SafeArea, Text, TextThemeStyle, View,
)
from flet_lottie import Lottie


async def build_view(page, ctx):
    working_content = Column([
        Text(
            "Estic treballant en això! 🚧",
            text_align="center",
            weight=FontWeight.W_900,
            theme_style=TextThemeStyle.TITLE_LARGE,
            width=page.width,
            color="#6b9e9f",
        ),
        Lottie(src="src/working.json"),
        Divider(),
        Text(
            "Aquesta funcionalitat encara està en desenvolupament.\n\n"
            "Estic treballant per oferir-te aquesta opció aviat!",
            text_align="center",
        ),
    ], height=page.height * 0.55, alignment=MainAxisAlignment.CENTER,
       horizontal_alignment="center")

    page.views.append(View(
        route='/configuracio/politica_privacitat',
        padding=0,
        bgcolor="#FFFCF1",
        controls=[
            AppBar(title=Text("Política de privacitat"), adaptive=True, bgcolor="#AAD7D9"),
            SafeArea(content=working_content),
        ],
    ))
