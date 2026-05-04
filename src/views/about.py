from flet import View, AppBar, SafeArea, Text, Divider, FontWeight, TextThemeStyle

def about_view(page):
    return View(
        route='/configuracio/sobre_app',
        padding=0,
        bgcolor="#FFFCF1",
        controls=[
            AppBar(title=Text("Sobre l'aplicació"), adaptive=True, bgcolor="#AAD7D9"),
            SafeArea(content=Text("NEAR HERE...", text_align="center", weight=FontWeight.W_900, theme_style=TextThemeStyle.DISPLAY_SMALL, width=page.width, color="#6b9e9f")),
            Text("Versió: 0.1.3", text_align="center", weight=FontWeight.W_300, theme_style=TextThemeStyle.BODY_SMALL, width=page.width),
            Divider(),
            Text("Fet per: Marc Lumbreras Torregrosa \n Fet com a part pràctica del Treball de Recerca a Batxillerat, 2024-2025", text_align="center", weight=FontWeight.W_300, theme_style=TextThemeStyle.BODY_SMALL, width=page.width)
        ]
    )