"""Selector de categories: /categories"""
from flet import (
    AppBar, Checkbox, Column, Colors, ElevatedButton,
    ExpansionTile, FontWeight, SafeArea, Text, TileAffinity, View,
)


async def build_view(page, ctx, Tags_amunt_safe):
    categories_sel = ctx.APP_SESSIONS[page].get("categories_sel")

    page.add(Tags_amunt_safe, ctx.stack_cards, ctx.botons)

    Categ_info = Column([
        ExpansionTile(
            title=Text("Menjar", weight=FontWeight.W_600),
            subtitle=Text("Restaurants, bars, cafeteries, etc.", weight=FontWeight.W_300),
            affinity=TileAffinity.LEADING,
            collapsed_text_color=Colors.BLACK,
            text_color=Colors.BLACK,
            controls=[
                Checkbox(label="General Menjar 🍴", adaptive=True, on_change=ctx.categ_check_sel),
                Checkbox(label="Panaderia 🥖", adaptive=True, on_change=ctx.categ_check_sel),
                Checkbox(label="Bar🍹", adaptive=True, on_change=ctx.categ_check_sel),
                Checkbox(label="Cafeteria ☕", adaptive=True, on_change=ctx.categ_check_sel),
                Checkbox(label="Creperia 🥞", adaptive=True, on_change=ctx.categ_check_sel),
                Checkbox(label="Botiga de postres 🥞", adaptive=True, on_change=ctx.categ_check_sel),
                Checkbox(label="Restaurants 🍴", adaptive=True, on_change=ctx.categ_check_sel),
                Checkbox(label="Restaurants 'Gluten-Free' ❌", adaptive=True, on_change=ctx.categ_check_sel),
            ],
        ),
        ExpansionTile(
            title=Text("Espais naturals", weight=FontWeight.W_600),
            subtitle=Text("Parcs, muntanyes, platges, llacs, etc.", weight=FontWeight.W_300),
            affinity=TileAffinity.LEADING,
            collapsed_text_color=Colors.BLACK,
            text_color=Colors.BLACK,
            controls=[
                Checkbox(label="General espais naturals 🏔️", adaptive=True, on_change=ctx.categ_check_sel),
                Checkbox(label="Platja 🏖️", adaptive=True, on_change=ctx.categ_check_sel),
                Checkbox(label="Monument 🏛️", adaptive=True, on_change=ctx.categ_check_sel),
                Checkbox(label="Parcs 🛝🌲", adaptive=True, on_change=ctx.categ_check_sel),
            ],
        ),
        ExpansionTile(
            title=Text("Botigues", weight=FontWeight.W_600),
            subtitle=Text("Botigues de roba, llibreries, centres comercials, etc.", weight=FontWeight.W_300),
            affinity=TileAffinity.LEADING,
            collapsed_text_color=Colors.BLACK,
            text_color=Colors.BLACK,
            controls=[
                Checkbox(label="General Botigues 🛍️", adaptive=True, on_change=ctx.categ_check_sel),
                Checkbox(label="Roba i moda 👜", adaptive=True, on_change=ctx.categ_check_sel),
                Checkbox(label="Centres comercials 🛒", adaptive=True, on_change=ctx.categ_check_sel),
                Checkbox(label="Llibreries 📚", adaptive=True, on_change=ctx.categ_check_sel),
                Checkbox(label="De conveniència 🏪", adaptive=True, on_change=ctx.categ_check_sel),
                Checkbox(label="Vintage i de segona mà 🛍️", adaptive=True, on_change=ctx.categ_check_sel),
                Checkbox(label="Flors i jardins 💐", adaptive=True, on_change=ctx.categ_check_sel),
                Checkbox(label="Joguines 🧸", adaptive=True, on_change=ctx.categ_check_sel),
                Checkbox(label="Menjar 🛒🍴", adaptive=True, on_change=ctx.categ_check_sel),
            ],
        ),
        ExpansionTile(
            title=Text("Entreteniment", weight=FontWeight.W_600),
            subtitle=Text("Inclou parcs d'atraccions, aquaris, arcades, galeries d'art, etc.",
                          weight=FontWeight.W_300),
            affinity=TileAffinity.LEADING,
            collapsed_text_color=Colors.BLACK,
            text_color=Colors.BLACK,
            controls=[
                Checkbox(label="General Entreteniment 🍿", adaptive=True, on_change=ctx.categ_check_sel),
                Checkbox(label="Museus 🖼️", adaptive=True, on_change=ctx.categ_check_sel),
                Checkbox(label="Karaoke 🎤", adaptive=True, on_change=ctx.categ_check_sel),
                Checkbox(label="Escape Room 🚪", adaptive=True, on_change=ctx.categ_check_sel),
                Checkbox(label="Bolera 🎳", adaptive=True, on_change=ctx.categ_check_sel),
                Checkbox(label="Cinema 🎥", adaptive=True, on_change=ctx.categ_check_sel),
                Checkbox(label="Parc d'atraccions 🎡🎢", adaptive=True, on_change=ctx.categ_check_sel),
            ],
        ),
        ExpansionTile(
            title=Text("Viatges", weight=FontWeight.W_600),
            subtitle=Text("Hotels, aeroports, estacions de tren, etc.", weight=FontWeight.W_300),
            affinity=TileAffinity.LEADING,
            collapsed_text_color=Colors.BLACK,
            text_color=Colors.BLACK,
            controls=[
                Checkbox(label="General viatges 🛩️", adaptive=True, on_change=ctx.categ_check_sel),
                Checkbox(label="Lloguer bicis 🚲", adaptive=True, on_change=ctx.categ_check_sel),
                Checkbox(label="Lloguer de barques 🚣🚣‍♀️", adaptive=True, on_change=ctx.categ_check_sel),
                Checkbox(label="Allotjament 🛌", adaptive=True, on_change=ctx.categ_check_sel),
                Checkbox(label="Parking 🅿️", adaptive=True, on_change=ctx.categ_check_sel),
                Checkbox(label="Àrea de descans ⌛", adaptive=True, on_change=ctx.categ_check_sel),
                Checkbox(label="Agència de viatges 🧳", adaptive=True, on_change=ctx.categ_check_sel),
            ],
        ),
    ])

    categ_info_add = Column(
        scroll="adaptive",
        height=page.height * 0.85,
        horizontal_alignment="center",
        controls=[
            Categ_info,
            ExpansionTile(
                title=Text("Turisme", weight=FontWeight.W_600),
                subtitle=Text("Que puc veure aqui?", weight=FontWeight.W_300),
                affinity=TileAffinity.LEADING,
                collapsed_text_color=Colors.BLACK,
                text_color=Colors.BLACK,
                controls=[
                    Text("Quan fas click al apartat de turisme, l'algorisme et detecta els millors "
                         "llocs per visitar a prop teu! 🧳🛩️🛌"),
                    Text("Ideal per viatges :)"),
                    Checkbox(label="Turisme 🧳🛩️🛌", adaptive=True,
                             on_change=ctx.categ_check_sel, label_position="center"),
                ],
            ),
            ElevatedButton("Tornar", bgcolor="#7cb7b9", color="black", on_click=ctx.view_pop),
        ],
    )

    # Restaura les categories prèviament seleccionades
    for category in Categ_info.controls:
        for i in range(len(category.controls)):
            if category.controls[i].label in ctx.categories_list:
                numeros_categ = ctx.categories_list[category.controls[i].label]
                for numero in numeros_categ:
                    if numero in categories_sel:
                        category.controls[i].value = True
                        category.initially_expanded = True

    page.views.append(View(
        route='/categories',
        padding=0,
        bgcolor="#FFFCF1",
        controls=[
            AppBar(title=Text("Categories"), adaptive=True, bgcolor="#AAD7D9"),
            SafeArea(content=categ_info_add),
        ],
    ))
