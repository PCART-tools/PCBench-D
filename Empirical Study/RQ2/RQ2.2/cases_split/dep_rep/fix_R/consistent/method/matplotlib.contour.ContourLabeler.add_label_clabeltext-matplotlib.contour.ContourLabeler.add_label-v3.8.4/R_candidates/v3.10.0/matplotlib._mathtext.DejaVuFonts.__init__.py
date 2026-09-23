    def __init__(self, default_font_prop: FontProperties, load_glyph_flags: LoadFlags):
        # This must come first so the backend's owner is set correctly
        if isinstance(self, DejaVuSerifFonts):
            self._fallback_font = StixFonts(default_font_prop, load_glyph_flags)
        else:
            self._fallback_font = StixSansFonts(default_font_prop, load_glyph_flags)
        self.bakoma = BakomaFonts(default_font_prop, load_glyph_flags)
        TruetypeFonts.__init__(self, default_font_prop, load_glyph_flags)
        # Include Stix sized alternatives for glyphs
        self._fontmap.update({
            1: 'STIXSizeOneSym',
            2: 'STIXSizeTwoSym',
            3: 'STIXSizeThreeSym',
            4: 'STIXSizeFourSym',
            5: 'STIXSizeFiveSym',
        })
        for key, name in self._fontmap.items():
            fullpath = findfont(name)
            self.fontmap[key] = fullpath
            self.fontmap[name] = fullpath
