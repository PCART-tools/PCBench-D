class DejaVuSansFonts(DejaVuFonts):
    """
    A font handling class for the DejaVu Sans fonts

    If a glyph is not found it will fallback to Stix Sans
    """
    _fontmap = {
        'rm': 'DejaVu Sans',
        'it': 'DejaVu Sans:italic',
        'bf': 'DejaVu Sans:weight=bold',
        'sf': 'DejaVu Sans',
        'tt': 'DejaVu Sans Mono',
        'ex': 'DejaVu Sans Display',
        0:    'DejaVu Sans',
    }
