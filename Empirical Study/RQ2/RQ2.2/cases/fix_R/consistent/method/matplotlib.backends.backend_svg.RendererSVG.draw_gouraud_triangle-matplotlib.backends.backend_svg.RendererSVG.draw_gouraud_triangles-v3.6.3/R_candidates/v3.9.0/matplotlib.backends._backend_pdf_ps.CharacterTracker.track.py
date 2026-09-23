    def track(self, font, s):
        """Record that string *s* is being typeset using font *font*."""
        char_to_font = font._get_fontmap(s)
        for _c, _f in char_to_font.items():
            self.used.setdefault(_f.fname, set()).add(ord(_c))
