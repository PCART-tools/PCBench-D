class CharacterTracker:
    """
    Helper for font subsetting by the pdf and ps backends.

    Maintains a mapping of font paths to the set of character codepoints that
    are being used from that font.
    """

    def __init__(self):
        self.used = {}

    def track(self, font, s):
        """Record that string *s* is being typeset using font *font*."""
        self.used.setdefault(font.fname, set()).update(map(ord, s))

    def track_glyph(self, font, glyph):
        """Record that codepoint *glyph* is being typeset using font *font*."""
        self.used.setdefault(font.fname, set()).add(glyph)
