def _font_supports_glyph(fonttype, glyph):
    """
    Returns True if the font is able to provide codepoint *glyph* in a PDF.

    For a Type 3 font, this method returns True only for single-byte
    characters. For Type 42 fonts this method return True if the character is
    from the Basic Multilingual Plane.
    """
    if fonttype == 3:
        return glyph <= 255
    if fonttype == 42:
        return glyph <= 65535
    raise NotImplementedError()
