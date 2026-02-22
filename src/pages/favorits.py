"""Pàgina de favorits: /favorits"""
from flet import Column, Container, Image, SafeArea, Text, View
from src.utils import convertir_url, resize_image_url


async def build_view(page, ctx):
    ctx.logger.info("Favorits seleccionat")
    saved_cards_images = await ctx.get_client_storage(page).get_async("saved_cards_images")
    saved_cards = await ctx.get_client_storage(page).get_async("saved_cards")
    categories_visited = await ctx.get_client_storage(page).get_async("categories_visited")

    ctx.images_saved.controls = []
    page.views.append(View(
        route='/favorits',
        padding=0,
        controls=[ctx.images_saved],
        bgcolor="#FFFCF1",
        navigation_bar=page.navigation_bar,
    ))

    if len(saved_cards) > 0:
        for i in range(len(saved_cards)):
            if saved_cards_images[i] != []:
                url = saved_cards_images[i]
                new_url = resize_image_url(url, 150, 150) if url.startswith(
                    "https://fastly.4sqi.net/img/general/"
                ) else url
                ctx.images_saved.controls.append(
                    Container(content=Column(
                        spacing=0.5,
                        horizontal_alignment="center",
                        controls=[
                            Image(src=new_url, border_radius=10),
                            Text(f"{saved_cards[i]['name']}", text_align="center"),
                        ],
                    ))
                )
                ctx.images_saved.controls.reverse()
                page.update()
            else:
                ctx.images_saved.controls.append(
                    Container(content=Column(
                        spacing=0.5,
                        horizontal_alignment="center",
                        controls=[
                            Image(src=convertir_url(categories_visited[i][0]), border_radius=10),
                            Text(f"{saved_cards[i]['name']}", text_align="center"),
                        ],
                    ))
                )
                page.update()
    else:
        page.views[-1].controls.append(
            SafeArea(content=Text(
                "No tens favorits!",
                text_align="center",
                height=page.height,
            ))
        )
