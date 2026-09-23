    def track(self, font, s):
        """Record that string *s* is being typeset using font *font*."""
        if isinstance(font, str):
            # Unused, can be removed after removal of track_characters.
            fname = font
        else:
            fname = font.fname
        self.used.setdefault(fname, set()).update(map(ord, s))
