    def __init__(self, default_font_prop: FontProperties, load_glyph_flags: LoadFlags):
        TruetypeFonts.__init__(self, default_font_prop, load_glyph_flags)
        for key, name in self._fontmap.items():
            fullpath = findfont(name)
            self.fontmap[key] = fullpath
            self.fontmap[name] = fullpath
