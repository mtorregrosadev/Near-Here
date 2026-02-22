"""Pàgina cerca a lloc específic: /lloc_especific"""
from flet import AppBar, BorderRadius, Icons, SafeArea, Text, TextField, View


async def build_view(page, ctx):
    def lloc_especific(e):
        ctx.logger.debug(e.control.value)
        ctx.APP_SESSIONS[page]["lloc_especific"] = e.control.value
        ctx.canvi = True

    page.views.append(View(
        route='/lloc_especific',
        padding=0,
        bgcolor="#FFFCF1",
        controls=[
            AppBar(title=Text("Cerca a un lloc"), adaptive=True, bgcolor="#AAD7D9"),
            SafeArea(content=Text(
                "Vols cercar a un lloc el qual no sigui el teu? "
                "Posa aqui el lloc i retorna a l'app per cercar!\n",
                width=page.width,
                text_align="center",
            )),
            TextField(
                on_change=lloc_especific,
                prefix_icon=Icons.SEARCH_OUTLINED,
                hint_text="Posa el lloc aqui",
                label="On vols cercar?",
                border_radius=BorderRadius.all(30),
                value=(
                    f"{ctx.APP_SESSIONS[page].get('lloc_especific')}"
                    if 'lloc_especific' in ctx.APP_SESSIONS[page]
                    else None
                ),
            ),
        ],
    ))
