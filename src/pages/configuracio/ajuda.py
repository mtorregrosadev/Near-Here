"""Ajuda: /configuracio/ajuda"""
from flet import AppBar, SafeArea, Text, View


async def build_view(page, ctx):
    page.views.append(View(
        route='/configuracio/ajuda',
        padding=0,
        bgcolor="#FFFCF1",
        controls=[
            AppBar(title=Text("Ajuda"), adaptive=True, bgcolor="#AAD7D9"),
            SafeArea(content=Text(
                "Qualsevol dubte o problema, no dubtis a contactar-me a l'e-mail:\n\n"
                "marquitorregrosa@gmail.com",
                width=page.width,
                text_align="center",
            )),
        ],
    ))
