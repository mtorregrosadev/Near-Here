from flet import (
    View, ListView, Container, Text, FontWeight, Row, ElevatedButton,
    Image, PagePlatform, Column, AlertDialog, Colors, InteractiveViewer,
    Margin, Stack, IconButton, Icons, ListTile, AppBar, Alignment, Icon
)
import logging
import datetime
import asyncio
from src.api_handlers import Llocs_info

logger = logging.getLogger('NearHere')

async def info_view(page, APP_SESSIONS, index_photo_stack, Foursquare, Yelp, Sostenible_L):
    # Get current data
    dadesLlocs = APP_SESSIONS[page].get("dadesLlocs")
    current_place = dadesLlocs[index_photo_stack]

    # Setup base layout containers  
    content = ListView(
        controls=[],
        auto_scroll=False,
        height=page.height*0.7,
    )

    # Header amb auto-ajust de mida de lletra segons height disponible (5% de la pantalla)
    def get_auto_font_size(text, height, min_size=18, max_size=36):
        # Ajusta la mida de la font segons la llargada del text i l'alçada disponible
        base = height * 0.7  # Augmenta el factor base per fer la lletra més gran
        length_factor = max(1, len(text) / 18)
        size = min(max(base / length_factor, min_size), max_size)
        # Si el text és molt llarg, redueix encara més la mida
        if len(text) > 22:
            size = max(size * 0.85, min_size)
        return size

    header_height = page.height * 0.07  
    header = Container(
        alignment = Alignment.CENTER,
        height=page.height * 0.085,
        width=page.width,
        content=Text(
            current_place['name'],
            text_align="center",
            weight=FontWeight.W_900,
            size=get_auto_font_size(current_place['name'], header_height),
            color="#6b9e9f",
            max_lines=2,
            overflow="ellipsis"
        ),
        padding=10,
    )
    
    # Afegim enllaços a aplicacions de mapes
    map_links = Row(
        alignment="center",
        spacing=10,
        controls=[],
        height=page.height*0.05,
    )
    obert_text =Text(
                "",
                width=page.width,
                size=10,
                text_align="center", # Add this to center the text
            )
    

    if current_place.get("geocodes", {}).get("main"):
        lat = current_place["geocodes"]["main"].get("latitude")
        lon = current_place["geocodes"]["main"].get("longitude")

    

    # Google Maps
    # Google Maps amb nom del lloc (si disponible)
    map_links.controls.append(
        ElevatedButton(
            content=Image(
                src="src/info/googleMaps.png",  
                width=24,
                height=24,
            ),
            tooltip="Google Maps",
            url=f"https://www.google.com/maps/search/?api=1&query={current_place['name'].replace(' ', '+')}&query_place_id=&query={lat},{lon}",
        )
    )
    
    # Waze
    map_links.controls.append(
        ElevatedButton(
            content=Image(
                src="src/info/WAZE.png",  
                width=24,
                height=24,
            ),
            tooltip="Waze",
            url=f"https://www.waze.com/ul?ll={lat}%2C{lon}&navigate=yes&zoom=17",
        ))
    logger.debug(page.platform)
    if PagePlatform.IOS:
        # Apple Maps (només per iOS)
        map_links.controls.append(
            ElevatedButton(
                content=Image(
                    src="src/info/AppleMaps.png",  
                    width=24,
                    height=24,
                ),
                tooltip="Apple Maps",
                url=f"maps://?q={lat},{lon}", #! Només funciona a iOS
            ))
        
    
    # Photo Carousel
    carousel = Column(
        alignment="center",
        controls=[]
    )
    
    photos = []
    # Obtenim les fotos depenent de la font de dades
    if current_place.get("photos"):
        # Cas Foursquare o Sostenible_L
        if isinstance(current_place["photos"], list):
            for photo in current_place["photos"]:
                if isinstance(photo, dict) and photo.get("prefix") and photo.get("suffix"):
                    photos.append(f"{photo['prefix']}original{photo['suffix']}")
                elif isinstance(photo, str):
                    photos.append(photo)
        # Cas Yelp
        elif isinstance(current_place["photos"], str):
            photos.append(current_place["photos"])
    async def imatge_en_gran(e):
        img_principal = main_image.content.content
        dlg = AlertDialog(
            bgcolor=Colors.with_opacity(0, '#ff6666'),
            content=InteractiveViewer(
                min_scale=0.1,
                max_scale=15,
                boundary_margin=Margin.all(20),
                content=Image(src=img_principal.src)
            )
        )
        page.open(dlg)
    if photos:
        logger.debug(photos)
        # Variable per seguir l'índex de la foto actual
        current_photo_index = 0
        # Imatge principal
        main_image = Container(
            alignment=Alignment.CENTER,
            on_click=imatge_en_gran,
            content=InteractiveViewer(
                min_scale=0.1,
                max_scale=15,
                content=Image(
                    src=photos[0],
                    width=page.width,
                    height=250,
                    fit="cover",
                    border_radius=10,
                    animate_opacity=150
                )
            )
        )
        
        # Comptador de fotos
        photo_counter = Text(
            f"1/{len(photos)}",
            color="#7A9A9C",
            size=12
        )
        
        # Funció per canviar la foto
        async def change_photo(e, direction):
            nonlocal current_photo_index, main_image, photo_counter
            
            if direction == "next":
                current_photo_index = (current_photo_index + 1) % len(photos)
            else:
                current_photo_index = (current_photo_index - 1) % len(photos)
            
            main_image.content.content.opacity = 0.1
            page.update()
            await asyncio.sleep(0.15)
            main_image.content.content.src = photos[current_photo_index]
            main_image.content.content.opacity = 1
            photo_counter.value = f"{current_photo_index + 1}/{len(photos)}"
            page.update()
        
        # Funcions d'event handler sense async
        async def prev_photo(e):
            await change_photo(e, "prev")
        
        async def next_photo(e):
            await change_photo(e, "next")
        
        # Contenidor pel carrusel
        carousel_container = Container(
            width=page.width,
            height=250,
            content=Stack(
                [
                    main_image,
                    # Botó esquerra
                    IconButton(
                        icon=Icons.CHEVRON_LEFT,
                        icon_color="black",
                        bgcolor="#FBF9F1",
                        on_click=prev_photo,
                        left=5,
                        top=100,
                        visible=len(photos) > 1
                    ),
                    # Botó dreta
                    IconButton(
                        icon=Icons.CHEVRON_RIGHT,
                        icon_color="black",
                        bgcolor="#FBF9F1",
                        on_click=next_photo,
                        right=5,
                        top=100,
                        visible=len(photos) > 1
                    ),
                    # Comptador de fotos
                    Container(
                        content=photo_counter,
                        bgcolor="#00000066",
                        padding=5,
                        border_radius=5,
                        right=10,
                        bottom=10,
                        visible=len(photos) > 1
                    )
                ]
            )
        )
        
        carousel.controls.append(carousel_container)
    else:
        # Sense fotos
        carousel.controls.append(
            Container(
                content=Icon(Icons.IMAGE_NOT_SUPPORTED_ROUNDED, size=100, color="#c9d6d7"),
                alignment=Alignment.CENTER,
                Margin=Margin.only(top=20, bottom=20)
            )
        )
        carousel.controls.append(
            Text("No hi ha imatges disponibles", text_align="center", color="#7A9A9C")
        )

    # Basic info section
    basic_info = Column(controls=[])
    
    # Add address if available
    if current_place.get("location", {}).get("address"):
        addr_parts = []
        if current_place["location"].get("address"): 
            addr_parts.append(current_place["location"]["address"])
        if current_place["location"].get("locality"):
            addr_parts.append(current_place["location"]["locality"])
        if current_place["location"].get("region"):
            addr_parts.append(current_place["location"]["region"])
        if current_place["location"].get("postcode"):
            addr_parts.append(current_place["location"]["postcode"])
            
        basic_info.controls.append(
            Container(
                content=Text(
                    "📍 " + ", ".join(addr_parts),
                    size=16,
                    weight=FontWeight.W_500
                ),
                Margin=Margin.only(bottom=10)
            )
        )
    # Alternativa per a Yelp
    elif current_place.get("location", {}).get("display_address"):
        if isinstance(current_place["location"]["display_address"], list):
            addr_text = ", ".join(current_place["location"]["display_address"])
        else:
            addr_text = current_place["location"]["display_address"]
            
        basic_info.controls.append(
            Container(
                content=Text(
                    "📍 " + addr_text,
                    size=16,
                    weight=FontWeight.W_500
                ),
                Margin=Margin.only(bottom=10)
            )
        )

    # Add categories if available
    if current_place.get("categories"):
        cats = []
        for cat in current_place["categories"]:
            if isinstance(cat, dict):
                cats.append(cat.get("title", cat.get("name", "")))
            else:
                cats.append(str(cat))
                
        basic_info.controls.append(
            Container(
                content=Text(
                    "🏷️ " + ", ".join(cats),
                    size=14
                ),
                Margin=Margin.only(bottom=10)
            )
        )
        
    # Add rating if available
    rating_row = Row(controls=[], alignment="center")
    
    if current_place.get("rating"):
        rating_value = current_place["rating"]
        # Normalitza la valoració a una escala 0-5 si és necessari
        if rating_value > 5:
            normalized_rating = round(rating_value / 2, 1)
        else:
            normalized_rating = rating_value
        
        stars = round(normalized_rating)
        
        for i in range(5):
            if i < stars:
                rating_row.controls.append(Icon(Icons.STAR_ROUNDED, color="#FFD700", size=20))
            else:
                rating_row.controls.append(Icon(Icons.STAR_OUTLINE_ROUNDED, color="#FFD700", size=20))
        
        rating_row.controls.append(Text(f" {normalized_rating}/5", weight=FontWeight.W_500))
        
        if current_place.get("review_count"):
            rating_row.controls.append(Text(f" ({current_place['review_count']} ressenyes)", size=12, color="grey"))
        
        basic_info.controls.append(
            Container(
                content=rating_row,
                Margin=Margin.only(bottom=10)
            )
        )
    logger.debug(current_place)
    # Add price level if available
    if current_place.get("price"):
        price_text = str(current_place["price"])
        logger.debug(price_text)
        price_desc = ""
        if price_text == "$" or price_text == "1":
            price_desc = "Econòmic"
        elif price_text == "$$" or price_text == "2":
            price_desc = "Moderat"
            logger.debug("Es 222")
        elif price_text == "$$$" or price_text == "3":
            price_desc = "Car"
        elif price_text == "$$$$" or price_text == "4":
            price_desc = "Molt car"
        
        if price_desc:
            basic_info.controls.append(
                Container(
                    content=Text(
                        f"💰 Preu: {price_desc} ({price_text}/4)",
                        size=14
                    ),
                    Margin=Margin.only(bottom=10)
                )
            )
            page.update()
    
    # Organitzem els elements en la vista principal
    content.controls.append(carousel)
    content.controls.append(
        Container(
            content=basic_info,
            Margin=Margin.only(top=10)
        )
    )
    
    # Contact info section
    contact = Column(controls=[])

    if Foursquare:
        # Get additional details for Foursquare
        info = Llocs_info(current_place['fsq_id'])
        details = await info.search_data()
        
        # Add phone
        if details.get('tel'):
            contact.controls.append(
                ListTile(
                    leading=Icon(Icons.PHONE),
                    title=Text(details['tel']),
                    url=f"tel:{details['tel']}"
                )
            )

        # Add email 
        if details.get('email'):
            contact.controls.append(
                ListTile(
                    leading=Icon(Icons.EMAIL),
                    title=Text(details['email']),
                    url=f"mailto:{details['email']}"
                )
            )
            
        # Add website
        if details.get('website'):
            contact.controls.append(
                ListTile(
                    leading=Icon(Icons.LANGUAGE),
                    title=Text("Lloc web"),
                    url=details['website']
                )
            )

        # Add social media
        if details.get('social_media'):
            social = Row(
                alignment="center",
                spacing=20,
                controls=[]
            )
            
            if details['social_media'].get('instagram'):
                social.controls.append(
                    ElevatedButton(
                        content=Image(
                            src="src/info/instagram.png",  
                            width=24,
                            height=24,
                        ),
                        tooltip="Instagram",
                        url=f"https://instagram.com/{details['social_media']['instagram']}",
                    )
                )
            
            if details['social_media'].get('twitter'):
                social.controls.append(
                    ElevatedButton(
                        content=Image(
                            src="src/info/twitter.png",  
                            width=24,
                            height=24,
                        ),
                        tooltip="Twitter", 
                        url=f"https://x.com/{details['social_media']['twitter']}",
                    )
                )
                
            if details['social_media'].get('facebook'):
                social.controls.append(
                    ElevatedButton(
                        content=Image(
                            src="src/info/facebook.png",  
                            width=24,
                            height=24,
                        ),
                        tooltip="Facebook",
                        url=f"https://facebook.com/{details['social_media']['facebook']}",
                    )
                )
                
            if social.controls:
                contact.controls.append(social)

        # Add hours if available
        if details.get('hours'):
            logger.debug(f"Hours: {details['hours']}")
            hours_controls = []
            if details['hours'].get('regular'):
                # Dictionary to map day numbers to Catalan day names
                day_names = {
                    1: 'Dilluns',
                    2: 'Dimarts', 
                    3: 'Dimecres',
                    4: 'Dijous',
                    5: 'Divendres',
                    6: 'Dissabte',
                    7: 'Diumenge'
                }

                # Get current day and time
                now = datetime.datetime.now()
                current_day = now.weekday() + 1  # weekday() returns 0-6, we need 1-7
                current_time = now.strftime('%H%M')

                # Check if place is open now
                is_open = False
                for day in details['hours']['regular']:
                    if day['day'] == current_day:
                        open_time = day['open'].replace(':', '')
                        close_time = day['close'].replace(':', '')
                        is_open = open_time <= current_time <= close_time
                        break

                hours_controls.append(
                    Text("Horari habitual:", weight=FontWeight.W_600)
                )
                for day in details['hours']['regular']:
                    # Format open time with :
                    open_time = f"{day['open'][:2]}:{day['open'][2:]}" if len(day['open']) == 4 else day['open']
                    # Format close time with :  
                    close_time = f"{day['close'][:2]}:{day['close'][2:]}" if len(day['close']) == 4 else day['close']
                    # Convert day number to name
                    day_name = day_names.get(day['day'], day['day'])
                    hours_controls.append(
                        Text(f"{day_name}: {open_time} - {close_time}")
                    )
                content.controls.append(
                    Container(
                        content=Column(controls=hours_controls),
                        Margin=Margin.only(top=20),
                        padding=10,
                        border_radius=10,
                        bgcolor=Colors.BLACK12
                    )
                )

            if details['hours'].get('open_now'):                 # Update obert_text based on open status
                obert_text.value = "OBERT" if is_open else "TANCAT"
                obert_text.color = "#4CAF50" if is_open else "#F44336" # Green if open, red if closed
                obert_text.weight = FontWeight.W_700
            elif details['hours'].get('regular'):
                # Si no tenim open_now, calculem si està obert segons l'horari regular
                now = datetime.datetime.now()
                current_day = now.weekday() + 1  # weekday() returns 0-6, we need 1-7
                current_time = now.strftime('%H%M')
                is_open = False
                for day in details['hours']['regular']:
                    if day['day'] == current_day:
                        open_time = day['open'].replace(':', '')
                        close_time = day['close'].replace(':', '')
                        if open_time <= current_time <= close_time:
                            is_open = True
                            break
                obert_text.value = "OBERT" if is_open else "TANCAT"
                obert_text.color = "#4CAF50" if is_open else "#F44336"
                obert_text.weight = FontWeight.W_700
        # Add stats if available
        if details.get('stats'):
            stats = Row(
                alignment="spaceAround",
                controls=[
                    Column([
                        Icon(Icons.STAR),
                        Text(f"{current_place["rating"]}")
                    ]),
                    Column([
                        Icon(Icons.PEOPLE), 
                        Text(f"{details['stats'].get('total_ratings', 'N/A')}")
                    ])
                ]
            )
            content.controls.append(
                Container(
                    content=stats,
                    Margin=Margin.only(top=10),
                    padding=10
                )
            )

        # Add menu if available
        if details.get('menu'):
            content.controls.append(
                Container(
                    content=ListTile(
                        leading=Icon(Icons.MENU_BOOK),
                        title=Text("Menú"),
                        url=details['menu'].get('url', '')
                    ),
                    Margin=Margin.only(top=10)
                )
            )

        # Add description if available
        if details.get('description'):
            content.controls.append(
                Container(
                    content=Text(details['description']),
                    Margin=Margin.only(top=20, bottom=20),
                    padding=10,
                    border_radius=10,
                    bgcolor=Colors.BLACK12
                )
            )

        # Add features/amenities if available
        if details.get('features'):
            features_list = Column([
                Text("Serveis disponibles:", weight=FontWeight.W_600)
            ])
            for feature, value in details['features'].items():
                if value:  # Only show enabled features
                    features_list.controls.append(
                        Text(f"✓ {feature.replace('_', ' ').title()}")
                    )
            content.controls.append(
                Container(
                    content=features_list,
                    Margin=Margin.only(top=10),
                    padding=10,
                    border_radius=10,
                    bgcolor=Colors.BLACK12
                )
            )

    elif Yelp:
        # Add Yelp specific fields
        if current_place.get('display_phone'):
            contact.controls.append(
                ListTile(
                    leading=Icon(Icons.PHONE),
                    title=Text(current_place['display_phone']),
                    url=f"tel:{current_place['phone']}"
                )
            )
            
        if current_place.get('url'):
            contact.controls.append(
                ListTile(
                    leading=Icon(Icons.LANGUAGE),
                    title=Text("Veure a Yelp"),
                    url=current_place['url']
                )
            )

    elif Sostenible_L:
        # Add sustainable place specific fields
        if current_place.get('details', {}).get('website'):
            contact.controls.append(
                ListTile(
                    leading=Icon(Icons.LANGUAGE),
                    title=Text("Lloc web"),
                    url=current_place['details']['website']
                )
            )
            
        if current_place.get('details', {}).get('type'):
            content.controls.append(
                Container(
                    content=Text(f"Tipus: {current_place['details']['type']}"),
                    Margin=Margin.only(top=10)
                )
            )
            
        if current_place.get('details', {}).get('criteria'):
            content.controls.append(
                Container(
                    content=Text(f"Criteris de sostenibilitat: {current_place['details']['criteria']}"),
                    Margin=Margin.only(top=10)
                )
            )

    if contact.controls:
        content.controls.append(
            Container(
                content=contact,
                Margin=Margin.only(top=20)
            )
        )

    return View(
            route='/info',
            padding=0,
            bgcolor="#FFFCF1",
            controls=[
                AppBar(bgcolor="#AAD7D9", adaptive=True),
                Container(
                    border_radius=10,
                    # Use a semi-transparent background color (e.g., 80% opacity)
                    bgcolor="#fff9f1",  # Add 'CC' for 80% opacity (hex: 0-FF)
                    width=page.width,
                    content=Column([
                        header,
                        obert_text,
                        map_links,
                        Text("")
                    ])
                ),
                content
            ]
    )
