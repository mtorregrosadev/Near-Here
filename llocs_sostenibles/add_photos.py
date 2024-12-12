import json
import requests

def is_image_url_valid(url):
    """
    Verifica si una URL és vàlida i serveix una imatge.
    """
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        content_type = response.headers.get("Content-Type", "")
        return response.status_code == 200 and "image" in content_type
    except Exception as e:
        print(f"Error verificant la URL: {e}")
        return False

def interactive_photo_input(data):
    """
    Permet a l'usuari introduir fotos per a un nombre específic de llocs que no tenen fotos.
    """
    print("Hola! Quants llocs vols emplenar avui?")
    try:
        total_places = int(input("Escriu el nombre de llocs que vols processar avui: "))
    except ValueError:
        print("Error: Has d'introduir un número vàlid. Per defecte processarem 5 llocs.")
        total_places = 5

    # Filtrar només els llocs que no tenen fotos
    places_without_photos = [place for place in data if 'photos' not in place or not place['photos']]
    total_places = min(total_places, len(places_without_photos))  # Limita als llocs disponibles sense fotos

    for index, item in enumerate(places_without_photos[:total_places]):
        print(f"\nLloc {index + 1}/{total_places}: {item['name']}")
        print(f"   - URL del lloc: {item['details']['website']}")
        print(f"   - Adreça: {item['details']['address']}")
        
        try:
            num_photos = int(input("Quantes fotos vols introduir per aquest lloc? "))
            photos = []
            for i in range(num_photos):
                photo_url = input(f"Introdueix la URL de la foto {i + 1}: ")
                if is_image_url_valid(photo_url):
                    photos.append(photo_url)
                else:
                    print("Aquesta URL no sembla vàlida per a una imatge. Introdueix-ne una altra.")
            
            # Afegir o actualitzar les fotos al lloc
            item['photos'] = photos
        except ValueError:
            print("Error: Has d'introduir un número vàlid. Continuem amb el següent lloc.")
    
    return data

# Camí al fitxer original
file_path = 'llocs_sostenibles.json'

# Carregar les dades existents
with open(file_path, 'r', encoding='utf-8') as file:
    markers_data = json.load(file)

# Passar les dades al procés interactiu
updated_markers = interactive_photo_input(markers_data)

# Sobreescriure el fitxer original amb les dades actualitzades
with open(file_path, 'w', encoding='utf-8') as file:
    json.dump(updated_markers, file, ensure_ascii=False, indent=4)

print(f"\nTotes les dades han estat actualitzades al fitxer original ({file_path})!")
