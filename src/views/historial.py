from flet import View, GridView, Container, Column, Image, Text, SafeArea, AppBar
from src.utils import resize_image_url, convertir_url

async def historial_view(page, get_client_storage):
    images_saved = GridView(
        expand=True,
        height=page.height, 
        runs_count=3,
        child_aspect_ratio=1,
        spacing=25,
        run_spacing=5
    )
    
    loc_visited = await get_client_storage(page).get_async("loc_visited")  
    loc_visited_photos = await get_client_storage(page).get_async("loc_visited_photos")  
    categories_visited = await get_client_storage(page).get_async("categories_visited")
    
    if loc_visited and len(loc_visited) > 0: 
        for i in range(len(loc_visited)):
            if loc_visited_photos[i] != []:
                url = loc_visited_photos[i][0]
                invariant_part = "https://fastly.4sqi.net/img/general/"
                if url.startswith(invariant_part):
                    new_url = resize_image_url(url, 150, 150)
                else:
                    new_url = url
                images_saved.controls.append(
                    Container(content=Column(spacing=0.5, horizontal_alignment="center", controls=[
                        Image(src=new_url, border_radius=10), 
                        Text(f"{loc_visited[i]['name']}", text_align="center")
                    ]))
                )
            else:
                cat_url = convertir_url(categories_visited[i][0]) if categories_visited and i < len(categories_visited) and categories_visited[i] else None
                if cat_url:
                    images_saved.controls.append(
                        Container(content=Column(spacing=0.5, horizontal_alignment="center", controls=[
                            Image(src=cat_url, border_radius=10), 
                            Text(f"{loc_visited[i]['name']}", text_align="center")
                        ]))
                    )
        images_saved.controls.reverse()
        
        return View(route='/configuracio/historial', padding=0, controls=[AppBar(title=Text("Historial de Llocs"), adaptive=True, bgcolor="#AAD7D9"), images_saved], bgcolor="#FFFCF1")
    else:
        return View(route='/configuracio/historial', padding=0, controls=[AppBar(title=Text("Historial de Llocs"), bgcolor="#AAD7D9", adaptive=True), SafeArea(content=Text("No has explorat cap lloc encara!", text_align="center", height=page.height))], bgcolor="#FFFCF1")
