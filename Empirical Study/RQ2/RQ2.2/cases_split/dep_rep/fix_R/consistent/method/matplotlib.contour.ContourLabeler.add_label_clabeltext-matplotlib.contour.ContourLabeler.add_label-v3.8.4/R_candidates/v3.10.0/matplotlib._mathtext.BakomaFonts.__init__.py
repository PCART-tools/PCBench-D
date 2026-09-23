    def __init__(self, default_font_prop: FontProperties, load_glyph_flags: LoadFlags):
        self._stix_fallback = StixFonts(default_font_prop, load_glyph_flags)

        super().__init__(default_font_prop, load_glyph_flags)
        for key, val in self._fontmap.items():
            fullpath = findfont(val)
            self.fontmap[key] = fullpath
            self.fontmap[val] = fullpath
