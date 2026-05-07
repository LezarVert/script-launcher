"""Module utilitaire pour charger des icônes emoji via PIL.

Utilise la police Noto Color Emoji pour rendre les emojis en images
compatibles avec Tcl/Tk (qui ne supporte pas les caractères Unicode
au-dessus de U+FFFF).
"""

import os
from PIL import Image, ImageDraw, ImageFont, ImageTk

# Chemin vers la police Noto Color Emoji
_FONT_PATH = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"
_emoji_font = None
_icon_cache = {}


def _get_font():
    """Charge la police emoji (singleton)."""
    global _emoji_font
    if _emoji_font is None:
        if os.path.exists(_FONT_PATH):
            _emoji_font = ImageFont.truetype(_FONT_PATH, 109)
        else:
            _emoji_font = ImageFont.load_default()
    return _emoji_font


def emoji_to_photo(emoji_char: str, size: int = 20) -> ImageTk.PhotoImage:
    """Convertit un caractère emoji en PhotoImage à la taille voulue.

    Args:
        emoji_char: Le caractère emoji à rendre (ex: '🚀')
        size: Taille en pixels de l'image résultante

    Returns:
        ImageTk.PhotoImage utilisable dans les widgets Tk
    """
    cache_key = (emoji_char, size)
    if cache_key in _icon_cache:
        return _icon_cache[cache_key]

    font = _get_font()
    img = Image.new("RGBA", (136, 136), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.text((4, 4), emoji_char, font=font, embedded_color=True)

    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)

    img = img.resize((size, size), Image.LANCZOS)
    photo = ImageTk.PhotoImage(img)
    _icon_cache[cache_key] = photo
    return photo


def load_app_icons(size_small: int = 18, size_medium: int = 24, size_large: int = 32):
    """Charge tous les icônes de l'application.

    Args:
        size_small: Taille pour les boutons d'action
        size_medium: Taille pour les labels/headers
        size_large: Taille pour les titres

    Returns:
        dict: Dictionnaire nom -> PhotoImage
    """
    icons = {}
    definitions = {
        # Titres et navigation
        "rocket": ("\U0001F680", size_large),
        "rocket_medium": ("\U0001F680", size_medium),
        # Éditeur
        "pencil": ("\U0001F4DD", size_medium),
        "save": ("\U0001F4BE", size_small),
        "run": ("\u25B6\uFE0F", size_small),
        "delete": ("\U0001F5D1\uFE0F", size_small),
        # Console
        "terminal": ("\U0001F4BB", size_medium),
        "clear": ("\U0001F5D1\uFE0F", size_small),
        # Liste de scripts
        "search": ("\U0001F50D", size_medium),
        "scroll": ("\U0001F4DC", size_medium),
        "new": ("\u2728", size_small),
        "python": ("\U0001F40D", size_small),
        "shell": ("\U0001F41A", size_small),
        # Dates
        "calendar": ("\U0001F4C5", size_small),
        "edit": ("\u270F\uFE0F", size_small),
        "played": ("\u25B6\uFE0F", size_small),
        # Thème
        "palette": ("\U0001F3A8", size_small),
        # Code
        "code": ("\U0001F4BB", size_medium),
        # Bienvenue
        "rocket_xl": ("\U0001F680", 80),
    }

    for name, (emoji, size) in definitions.items():
        try:
            icons[name] = emoji_to_photo(emoji, size)
        except Exception:
            # Fallback: image transparente
            img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
            icons[name] = ImageTk.PhotoImage(img)

    return icons
