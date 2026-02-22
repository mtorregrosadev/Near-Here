"""Detall d'un lloc: /info"""
import asyncio
import datetime
import flet
from flet import (
    AlertDialog, AppBar, Column, Colors, Container, ElevatedButton,
    FontWeight, Icon, Icons, Image, InteractiveViewer, ListTile,
    Margin, PagePlatform, Row, Text, View,
)
from scripts.llocs import Llocs_info


async def build_view(page, ctx):
    ctx.logger.info("=== RUTA: /info ===")
    dadesLlocs = ctx.APP_SESSIONS[page].get("dadesLlocs")
    current_place = dadesLlocs[ctx.index_photo_stack]

    content = flet.ListView(controls=[], auto_scroll=False, height=page.height * 0.7)

    # ── Header ────────────────────────────────────────────────────────
    def get_auto_font_size(text, height, min_size=18, max_size=36):
        base = height * 0.7
        length_factor = max(1, len(text) / 18)
        size = min(max(base / length_factor, min_size), max_size)
        if len(text) > 22:
            size = max(size * 0.85, min_size)
        return size

    header_height = page.height * 0.07
    header = Container(
        alignment=flet.Alignment.CENTER,
        height=page.height * 0.085,
        width=page.width,
        content=Text(
            current_place['name'],
            text_align="center",
            weight=FontWeight.W_900,
            size=get_auto_font_size(current_place['name'], header_height),
            color="#6b9e9f",
            max_lines=2,
            overflow="ellipsis",
        ),
        padding=10,
    )

    # ── Map links ─────────────────────────────────────────────────────
    map_links = Row(alignment="center", spacing=10, controls=[], height=page.height * 0.05)
    obert_text = Text("", width=page.width, size=10, text_align="center")

    lat = lon = None
    if current_place.get("geocodes", {}).get("main"):
        lat = current_place["geocodes"]["main"].get("latitude")
        lon = current_place["geocodes"]["main"].get("longitude")

    map_links.controls.append(ElevatedButton(
        content=Image(src="src/info/googleMaps.png", width=24, height=24),
        tooltip="Google Maps",
        url=(f"https://www.google.com/maps/search/?api=1&query="
             f"{current_place['name'].replace(' ', '+')}&query_place_id=&query={lat},{lon}"),
    ))
    map_links.controls.append(ElevatedButton(
        content=Image(src="src/info/WAZE.png", width=24, height=24),
        tooltip="Waze",
        url=f"https://www.waze.com/ul?ll={lat}%2C{lon}&navigate=yes&zoom=17",
    ))
    ctx.logger.debug(page.platform)
    if PagePlatform.IOS:
        map_links.controls.append(ElevatedButton(
            content=Image(src="src/info/AppleMaps.png", width=24, height=24),
            tooltip="Apple Maps",
            url=f"maps://?q={lat},{lon}",
        ))

    # ── Photo carousel ────────────────────────────────────────────────
    carousel = Column(alignment="center", controls=[])
    photos = []
    if current_place.get("photos"):
        if isinstance(current_place["photos"], list):
            for photo in current_place["photos"]:
                if isinstance(photo, dict) and photo.get("prefix") and photo.get("suffix"):
                    photos.append(f"{photo['prefix']}original{photo['suffix']}")
                elif isinstance(photo, str):
                    photos.append(photo)
        elif isinstance(current_place["photos"], str):
            photos.append(current_place["photos"])

    async def imatge_en_gran(e):
        img_principal = main_image.content.content
        dlg = AlertDialog(
            bgcolor=Colors.with_opacity(0, '#ff6666'),
            content=InteractiveViewer(
                min_scale=0.1, max_scale=15,
                boundary_margin=Margin.all(20),
                content=Image(src=img_principal.src),
            ),
        )
        page.open(dlg)

    if photos:
        ctx.logger.debug(photos)
        current_photo_index = 0
        main_image = Container(
            alignment=flet.Alignment.CENTER,
            on_click=imatge_en_gran,
            content=InteractiveViewer(
                min_scale=0.1, max_scale=15,
                content=Image(
                    src=photos[0],
                    width=page.width,
                    height=250,
                    fit="cover",
                    border_radius=10,
                    animate_opacity=150,
                ),
            ),
        )
        photo_counter = Text(f"1/{len(photos)}", color="#7A9A9C", size=12)

        async def change_photo(e, direction):
            nonlocal current_photo_index
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

        async def prev_photo(e):
            await change_photo(e, "prev")

        async def next_photo(e):
            await change_photo(e, "next")

        carousel_container = Container(
            width=page.width, height=250,
            content=flet.Stack([
                main_image,
                flet.IconButton(
                    icon=Icons.CHEVRON_LEFT, icon_color="black", bgcolor="#FBF9F1",
                    on_click=prev_photo, left=5, top=100, visible=len(photos) > 1,
                ),
                flet.IconButton(
                    icon=Icons.CHEVRON_RIGHT, icon_color="black", bgcolor="#FBF9F1",
                    on_click=next_photo, right=5, top=100, visible=len(photos) > 1,
                ),
                Container(
                    content=photo_counter, bgcolor="#00000066", padding=5,
                    border_radius=5, right=10, bottom=10, visible=len(photos) > 1,
                ),
            ]),
        )
        carousel.controls.append(carousel_container)
    else:
        carousel.controls.append(Container(
            content=Icon(Icons.IMAGE_NOT_SUPPORTED_ROUNDED, size=100, color="#c9d6d7"),
            alignment=flet.Alignment.CENTER,
            Margin=Margin.only(top=20, bottom=20),
        ))
        carousel.controls.append(
            Text("No hi ha imatges disponibles", text_align="center", color="#7A9A9C")
        )

    # ── Basic info ────────────────────────────────────────────────────
    basic_info = Column(controls=[])

    if current_place.get("location", {}).get("address"):
        addr_parts = []
        loc = current_place["location"]
        for key in ("address", "locality", "region", "postcode"):
            if loc.get(key):
                addr_parts.append(loc[key])
        basic_info.controls.append(Container(
            content=Text("📍 " + ", ".join(addr_parts), size=16, weight=FontWeight.W_500),
            Margin=Margin.only(bottom=10),
        ))
    elif current_place.get("location", {}).get("display_address"):
        addr = current_place["location"]["display_address"]
        addr_text = ", ".join(addr) if isinstance(addr, list) else addr
        basic_info.controls.append(Container(
            content=Text("📍 " + addr_text, size=16, weight=FontWeight.W_500),
            Margin=Margin.only(bottom=10),
        ))

    if current_place.get("categories"):
        cats = []
        for cat in current_place["categories"]:
            if isinstance(cat, dict):
                cats.append(cat.get("title", cat.get("name", "")))
            else:
                cats.append(str(cat))
        basic_info.controls.append(Container(
            content=Text("🏷️ " + ", ".join(cats), size=14),
            Margin=Margin.only(bottom=10),
        ))

    rating_row = Row(controls=[], alignment="center")
    if current_place.get("rating"):
        rating_value = current_place["rating"]
        normalized_rating = round(rating_value / 2, 1) if rating_value > 5 else rating_value
        stars = round(normalized_rating)
        for i in range(5):
            rating_row.controls.append(Icon(
                Icons.STAR_ROUNDED if i < stars else Icons.STAR_OUTLINE_ROUNDED,
                color="#FFD700", size=20,
            ))
        rating_row.controls.append(Text(f" {normalized_rating}/5", weight=FontWeight.W_500))
        if current_place.get("review_count"):
            rating_row.controls.append(
                Text(f" ({current_place['review_count']} ressenyes)", size=12, color="grey")
            )
        basic_info.controls.append(Container(content=rating_row, Margin=Margin.only(bottom=10)))

    ctx.logger.debug(current_place)
    if current_place.get("price"):
        price_text = str(current_place["price"])
        ctx.logger.debug(price_text)
        price_desc = {"$": "Econòmic", "1": "Econòmic",
                      "$$": "Moderat", "2": "Moderat",
                      "$$$": "Car", "3": "Car",
                      "$$$$": "Molt car", "4": "Molt car"}.get(price_text, "")
        if price_desc:
            basic_info.controls.append(Container(
                content=Text(f"💰 Preu: {price_desc} ({price_text}/4)", size=14),
                Margin=Margin.only(bottom=10),
            ))
            page.update()

    content.controls.append(carousel)
    content.controls.append(Container(content=basic_info, Margin=Margin.only(top=10)))

    # ── Contact / extended info ────────────────────────────────────────
    contact = Column(controls=[])

    if ctx.Foursquare:
        info = Llocs_info(current_place['fsq_id'])
        details = await info.search_data()

        if details.get('tel'):
            contact.controls.append(ListTile(
                leading=Icon(Icons.PHONE), title=Text(details['tel']),
                url=f"tel:{details['tel']}",
            ))
        if details.get('email'):
            contact.controls.append(ListTile(
                leading=Icon(Icons.EMAIL), title=Text(details['email']),
                url=f"mailto:{details['email']}",
            ))
        if details.get('website'):
            contact.controls.append(ListTile(
                leading=Icon(Icons.LANGUAGE), title=Text("Lloc web"),
                url=details['website'],
            ))
        if details.get('social_media'):
            social = Row(alignment="center", spacing=20, controls=[])
            sm = details['social_media']
            if sm.get('instagram'):
                social.controls.append(ElevatedButton(
                    content=Image(src="src/info/instagram.png", width=24, height=24),
                    tooltip="Instagram",
                    url=f"https://instagram.com/{sm['instagram']}",
                ))
            if sm.get('twitter'):
                social.controls.append(ElevatedButton(
                    content=Image(src="src/info/twitter.png", width=24, height=24),
                    tooltip="Twitter",
                    url=f"https://x.com/{sm['twitter']}",
                ))
            if sm.get('facebook'):
                social.controls.append(ElevatedButton(
                    content=Image(src="src/info/facebook.png", width=24, height=24),
                    tooltip="Facebook",
                    url=f"https://facebook.com/{sm['facebook']}",
                ))
            if social.controls:
                contact.controls.append(social)

        if details.get('hours'):
            ctx.logger.debug(f"Hours: {details['hours']}")
            hours_controls = []
            day_names = {1: 'Dilluns', 2: 'Dimarts', 3: 'Dimecres', 4: 'Dijous',
                         5: 'Divendres', 6: 'Dissabte', 7: 'Diumenge'}
            now = datetime.datetime.now()
            current_day = now.weekday() + 1
            current_time = now.strftime('%H%M')

            if details['hours'].get('regular'):
                is_open = False
                for day in details['hours']['regular']:
                    if day['day'] == current_day:
                        o = day['open'].replace(':', '')
                        c = day['close'].replace(':', '')
                        is_open = o <= current_time <= c
                        break

                hours_controls.append(Text("Horari habitual:", weight=FontWeight.W_600))
                for day in details['hours']['regular']:
                    open_t = f"{day['open'][:2]}:{day['open'][2:]}" if len(day['open']) == 4 else day['open']
                    close_t = f"{day['close'][:2]}:{day['close'][2:]}" if len(day['close']) == 4 else day['close']
                    hours_controls.append(
                        Text(f"{day_names.get(day['day'], day['day'])}: {open_t} - {close_t}")
                    )
                content.controls.append(Container(
                    content=Column(controls=hours_controls),
                    Margin=Margin.only(top=20), padding=10,
                    border_radius=10, bgcolor=Colors.BLACK12,
                ))

            if details['hours'].get('open_now'):
                obert_text.value = "OBERT" if is_open else "TANCAT"
                obert_text.color = "#4CAF50" if is_open else "#F44336"
                obert_text.weight = FontWeight.W_700
            elif details['hours'].get('regular'):
                is_open = False
                for day in details['hours']['regular']:
                    if day['day'] == current_day:
                        o = day['open'].replace(':', '')
                        c = day['close'].replace(':', '')
                        if o <= current_time <= c:
                            is_open = True
                            break
                obert_text.value = "OBERT" if is_open else "TANCAT"
                obert_text.color = "#4CAF50" if is_open else "#F44336"
                obert_text.weight = FontWeight.W_700

        if details.get('stats'):
            stats = Row(
                alignment="spaceAround",
                controls=[
                    Column([Icon(Icons.STAR), Text(f"{current_place['rating']}")]),
                    Column([Icon(Icons.PEOPLE),
                            Text(f"{details['stats'].get('total_ratings', 'N/A')}")]),
                ],
            )
            content.controls.append(Container(
                content=stats, Margin=Margin.only(top=10), padding=10,
            ))

        if details.get('menu'):
            content.controls.append(Container(
                content=ListTile(
                    leading=Icon(Icons.MENU_BOOK), title=Text("Menú"),
                    url=details['menu'].get('url', ''),
                ),
                Margin=Margin.only(top=10),
            ))

        if details.get('description'):
            content.controls.append(Container(
                content=Text(details['description']),
                Margin=Margin.only(top=20, bottom=20), padding=10,
                border_radius=10, bgcolor=Colors.BLACK12,
            ))

        if details.get('features'):
            features_list = Column([Text("Serveis disponibles:", weight=FontWeight.W_600)])
            for feature, value in details['features'].items():
                if value:
                    features_list.controls.append(
                        Text(f"✓ {feature.replace('_', ' ').title()}")
                    )
            content.controls.append(Container(
                content=features_list, Margin=Margin.only(top=10), padding=10,
                border_radius=10, bgcolor=Colors.BLACK12,
            ))

    elif ctx.Yelp:
        if current_place.get('display_phone'):
            contact.controls.append(ListTile(
                leading=Icon(Icons.PHONE), title=Text(current_place['display_phone']),
                url=f"tel:{current_place['phone']}",
            ))
        if current_place.get('url'):
            contact.controls.append(ListTile(
                leading=Icon(Icons.LANGUAGE), title=Text("Veure a Yelp"),
                url=current_place['url'],
            ))

    elif ctx.Sostenible_L:
        if current_place.get('details', {}).get('website'):
            contact.controls.append(ListTile(
                leading=Icon(Icons.LANGUAGE), title=Text("Lloc web"),
                url=current_place['details']['website'],
            ))
        if current_place.get('details', {}).get('type'):
            content.controls.append(Container(
                content=Text(f"Tipus: {current_place['details']['type']}"),
                Margin=Margin.only(top=10),
            ))
        if current_place.get('details', {}).get('criteria'):
            content.controls.append(Container(
                content=Text(f"Criteris de sostenibilitat: {current_place['details']['criteria']}"),
                Margin=Margin.only(top=10),
            ))

    if contact.controls:
        content.controls.append(Container(content=contact, Margin=Margin.only(top=20)))

    page.views.append(View(
        route='/info',
        padding=0,
        bgcolor="#FFFCF1",
        controls=[
            AppBar(bgcolor="#AAD7D9", adaptive=True),
            Container(
                border_radius=10,
                bgcolor="#fff9f1",
                width=page.width,
                content=Column([header, obert_text, map_links, Text("")]),
            ),
            content,
        ],
    ))
