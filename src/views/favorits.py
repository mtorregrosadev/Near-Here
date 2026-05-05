from flet import View, GridView, Container, Column, Image, Text, SafeArea, padding
from src.utils import resize_image_url, convertir_url

async def favorits_view(page, get_client_storage):
    images_saved = GridView(
        expand=True,
        height=page.height * 0.89, 
        runs_count=3,
        child_aspect_ratio=1,
        spacing=25,
        run_spacing=5
    )
    
    saved_cards_images = await get_client_storage(page).get_async("saved_cards_images")   
    saved_cards = await get_client_storage(page).get_async("saved_cards")
    categories_visited = await get_client_storage(page).get_async("categories_visited")
    
    view = View(
        route='/favorits',
        padding=0,
        controls=[images_saved],
        bgcolor="#FFFCF1",
        navigation_bar=page.navigation_bar
    )
    
    if saved_cards and len(saved_cards) > 0:
        for i in range(len(saved_cards)):
            if saved_cards_images[i] != []: 
                url = saved_cards_images[i]
                if url.startswith("https://fastly.4sqi.net/img/general/"):
                    new_url = resize_image_url(url, 150, 150)
                else:
                    new_url = url
                images_saved.controls.append(
                    Container(content=Column(spacing=0.5, horizontal_alignment="center", controls=[
                        Image(src=new_url, border_radius=10), 
                        Text(f"{saved_cards[i]['name']}", text_align="center")
                    ]))
                )
                images_saved.controls.reverse()
            else:
                cat_url = convertir_url(categories_visited[i][0]) if categories_visited and i < len(categories_visited) and categories_visited[i] else None
                if cat_url:
                    images_saved.controls.append(
                        Container(content=Column(spacing=0.5, horizontal_alignment="center", controls=[
                            Image(src=cat_url, border_radius=10), 
                            Text(f"{saved_cards[i]['name']}", text_align="center")
                        ]))
                    )
    else:
        view.controls.append(SafeArea(content=Text("No tens favorits!", text_align="center", height=page.height)))
        
    return view
