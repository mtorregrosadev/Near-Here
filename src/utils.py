"""
Shared URL helper utilities used by multiple page modules.
"""


def resize_image_url(url: str, width: int, height: int) -> str:
    """Resize a Foursquare image URL to the given dimensions."""
    invariant_part = "https://fastly.4sqi.net/img/general/"
    start_index = len(invariant_part)
    variable_part = url[start_index:]
    _dimensions, remainder = variable_part.split('/', 1)
    new_url = invariant_part + f'{width}x{height}' + '/' + remainder
    return new_url


def convertir_url(url: str) -> str:
    """Add the '_bg' suffix to a category icon URL if not already present."""
    parts = url.split('/')
    filename = parts[-1]
    filename_parts = filename.split('_')
    if 'bg' not in filename_parts:
        filename_parts.insert(-1, 'bg')
    parts[-1] = '_'.join(filename_parts)
    return '/'.join(parts)
