    def track(self, font, s):
        """Record that string *s* is being typeset using font *font*."""
        self.used.setdefault(font.fname, set()).update(map(ord, s))
