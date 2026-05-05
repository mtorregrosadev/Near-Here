from flet import (
    Page,
    View,
    Column,
    Text,
    Divider,
    FontWeight,
    TextThemeStyle,
    MainAxisAlignment,
    SafeArea,
    AppBar,
    RadioGroup,
    Radio,
    TextField,
    BorderRadius,
    Icons
)
from flet_lottie import Lottie

def under_construction_view(page: Page, title: str, route: str):
    """Vista genèrica per a qualsevol apartat en obres."""
    working_content = Column([
        Text("Estic treballant en això! 🚧", text_align="center", weight=FontWeight.W_900, theme_style=TextThemeStyle.TITLE_LARGE, width=page.width, color="#6b9e9f"),
        Lottie(src="src/working.json"),
        Divider(),
        Text("Aquesta funcionalitat encara està en desenvolupament.\n\nEstic treballant per oferir-te aquesta opció aviat!", text_align="center")
    ], height=page.height*0.55, alignment=MainAxisAlignment.CENTER, horizontal_alignment="center")
    
    return View(
        route=route, 
        padding=0, 
        bgcolor="#FFFCF1",
        controls=[
            AppBar(title=Text(title), adaptive=True, bgcolor="#AAD7D9"), 
            SafeArea(content=working_content)
        ]
    )

def ajuda_view(page: Page):
    return View(
        route='/configuracio/ajuda', 
        padding=0, 
        bgcolor="#FFFCF1",
        controls=[
            AppBar(title=Text("Ajuda"), adaptive=True, bgcolor="#AAD7D9"), 
            SafeArea(content=Text("Qualsevol dubte o problema, no dubtis a contactar-me a l'e-mail:\n\nmarquitorregrosa@gmail.com", width=page.width, text_align="center"))
        ]
    )

def idioma_view(page: Page, APP_SESSIONS, idioma_canviat_callback):
    idioma = APP_SESSIONS[page].get("idioma", "")
    return View(
        route='/configuracio/idioma', 
        padding=0, 
        bgcolor="#FFFCF1",
        controls=[
            AppBar(title=Text("Idioma"), adaptive=True, bgcolor="#AAD7D9"),
            SafeArea(content=Text("Recorda que l'idioma de moment es només de la IA! No canvia l'idioma de l'app!!", width=page.width, text_align="center")),
            RadioGroup(
                content=Column([
                    Radio(value="Català", label="Català"),
                    Radio(value="Castellano", label="Castellano"),
                    Radio(value="English", label="English")
                ]), 
                on_change=idioma_canviat_callback, 
                value=f"{idioma}"
            )
        ]
    )

def lloc_especific_view(page: Page, APP_SESSIONS, lloc_especific_callback):
    valor_actual = APP_SESSIONS[page].get('lloc_especific')
    
    return View(
        route='/lloc_especific', 
        padding=0, 
        bgcolor="#FFFCF1",
        controls=[
            AppBar(title=Text("Cerca a un lloc"), adaptive=True, bgcolor="#AAD7D9"), 
            SafeArea(content=Text("Vols cercar a un lloc el qual no sigui el teu? Posa aqui el lloc i retorna a l'app per cercar!\n", width=page.width, text_align="center")),
            TextField(
                on_change=lloc_especific_callback, 
                prefix_icon=Icons.SEARCH_OUTLINED, 
                hint_text="Posa el lloc aqui", 
                label="On vols cercar?", 
                border_radius=BorderRadius.all(30), 
                value=f"{valor_actual}" if valor_actual else None
            )
        ]
    )


