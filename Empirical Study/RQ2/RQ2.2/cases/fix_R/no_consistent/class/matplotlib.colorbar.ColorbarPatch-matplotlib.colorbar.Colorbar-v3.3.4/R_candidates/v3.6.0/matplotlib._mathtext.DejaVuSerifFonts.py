class DejaVuSerifFonts(DejaVuFonts):
    """
    A font handling class for the DejaVu Serif fonts

    If a glyph is not found it will fallback to Stix Serif
    """
    _fontmap = {
        'rm': 'DejaVu Serif',
        'it': 'DejaVu Serif:italic',
        'bf': 'DejaVu Serif:weight=bold',
        'sf': 'DejaVu Sans',
        'tt': 'DejaVu Sans Mono',
        'ex': 'DejaVu Serif Display',
        0:    'DejaVu Serif',
    }
