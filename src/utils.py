def resize_image_url(url, width, height):
    # Part invariable de l'URL
    invariant_part = "https://fastly.4sqi.net/img/general/"
    
    # Busca la posició on comença la part variable (les dimensions i la resta de l'URL)
    start_index = len(invariant_part)
    
    # Obté la part variable de l'URL
    variable_part = url[start_index:]
    
    # Busca la primera part que coincideix amb el patró 'widthxheight'
    dimensions, remainder = variable_part.split('/', 1)
    
    # Substitueix les dimensions per les noves
    new_dimensions = f'{width}x{height}'
    
    # Construeix la nova URL
    new_url = invariant_part + new_dimensions + '/' + remainder
    
    return new_url

def convertir_url(url):
    parts = url.split('/')
    filename = parts[-1]
    filename_parts = filename.split('_')
        
    # Si no té ja el sufix "_bg", l'afegim abans del número.
    if 'bg' not in filename_parts:
        filename_parts.insert(-1, 'bg')
        
    # Reconstruïm el nom del fitxer
    new_filename = '_'.join(filename_parts)
    parts[-1] = new_filename
        
    # Reconstruïm la URL completa
    return '/'.join(parts)