class CharacterTracker:
    """
    Helper for font subsetting by the pdf and ps backends.

    Maintains a mapping of font paths to the set of character codepoints that
    are being used from that font.
    """

    def __init__(self):
        self.used = {}

    @_api.deprecated("3.3")
    @property
    def used_characters(self):
        d = {}
        for fname, chars in self.used.items():
            realpath, stat_key = mpl.cbook.get_realpath_and_stat(fname)
            d[stat_key] = (realpath, chars)
        return d

    def track(self, font, s):
        """Record that string *s* is being typeset using font *font*."""
        if isinstance(font, str):
            # Unused, can be removed after removal of track_characters.
            fname = font
        else:
            fname = font.fname
        self.used.setdefault(fname, set()).update(map(ord, s))

    # Not public, can be removed when pdf/ps merge_used_characters is removed.
    def merge(self, other):
        """Update self with a font path to character codepoints."""
        for fname, charset in other.items():
            self.used.setdefault(fname, set()).update(charset)
