import asyncio
import os
from flet_lottie import Lottie
from src.constants import get_system_instructions

async def ia_view_setup(page, APP_SESSIONS, ia_container, first_message):
    await page.push_route('/')
    ai = 2
    anim_carrega = Lottie(src="src/ia_animation.json", repeat=True)   
    page.overlay.append(ia_container)
    page.update()
    ia_container.content.controls[0].content.controls[1].controls.append(anim_carrega)
    ia_container.update()
    await asyncio.sleep(0.1)
    
    dadesLlocs = APP_SESSIONS[page].get("dadesLlocs")
    idioma = APP_SESSIONS[page].get("idioma")
    user_categories = APP_SESSIONS[page].get("categories_sel")
    system_instructions = get_system_instructions(dadesLlocs, idioma, user_categories)
    
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is not set or is empty.")
    
    # We trigger the first message which does the actual work
    await first_message()
