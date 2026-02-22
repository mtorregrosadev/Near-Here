"""Historial de llocs visitats: /configuracio/historial"""
from flet import AppBar, Column, Container, Image, SafeArea, Text, View
from src.utils import convertir_url, resize_image_url


async def build_view(page, ctx):
    loc_visited = await ctx.get_client_storage(page).get_async("loc_visited")
    loc_visited_photos = await ctx.get_client_storage(page).get_async("loc_visited_photos")
    categories_visited = await ctx.get_client_storage(page).get_async("categories_visited")

    ctx.logger.debug(f"loc_visited len: {len(loc_visited)}")
    ctx.images_saved.height = page.height
    ctx.images_saved.controls = []

    invariant_part = "https://fastly.4sqi.net/img/general/"

    if len(loc_visited) > 0:
        page.views.append(View(
            route='/configuracio/historial',
            padding=0,
            controls=[
                AppBar(title=Text("Historial de Llocs"), adaptive=True, bgcolor="#AAD7D9"),
                ctx.images_saved,
            ],
            bgcolor="#FFFCF1",
        ))
        for i in range(len(loc_visited)):
            if loc_visited_photos[i] != []:
                url = loc_visited_photos[i][0]
                new_url = resize_image_url(url, 150, 150) if url.startswith(invariant_part) else url
                ctx.images_saved.controls.append(
                    Container(content=Column(
                        spacing=0.5,
                        horizontal_alignment="center",
                        controls=[
                            Image(src=new_url, border_radius=10),
                            Text(f"{loc_visited[i]['name']}", text_align="center"),
                        ],
                    ))
                )
                page.update()
            else:
                ctx.images_saved.controls.append(
                    Container(content=Column(
                        spacing=0.5,
                        horizontal_alignment="center",
                        controls=[
                            Image(src=convertir_url(categories_visited[i][0]), border_radius=10),
                            Text(f"{loc_visited[i]['name']}", text_align="center"),
                        ],
                    ))
                )
                page.update()
        ctx.images_saved.controls.reverse()
    else:
        page.views.append(View(
            route='/configuracio/historial',
            padding=0,
            controls=[
                AppBar(title=Text("Historial de Llocs"), bgcolor="#AAD7D9", adaptive=True),
                SafeArea(content=Text(
                    "No has explorat cap lloc encara!",
                    text_align="center",
                    height=page.height,
                )),
            ],
            bgcolor="#FFFCF1",
        ))
