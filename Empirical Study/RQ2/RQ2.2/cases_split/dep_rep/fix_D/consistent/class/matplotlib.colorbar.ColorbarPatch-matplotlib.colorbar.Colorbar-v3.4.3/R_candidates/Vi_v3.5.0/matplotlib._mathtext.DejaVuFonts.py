class DejaVuFonts(UnicodeFonts):
    use_cmex = False  # Unused; delete once mathtext becomes private.

    def __init__(self, *args, **kwargs):
        # This must come first so the backend's owner is set correctly
        if isinstance(self, DejaVuSerifFonts):
            self.cm_fallback = StixFonts(*args, **kwargs)
        else:
            self.cm_fallback = StixSansFonts(*args, **kwargs)
        self.bakoma = BakomaFonts(*args, **kwargs)
        TruetypeFonts.__init__(self, *args, **kwargs)
        self.fontmap = {}
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

    def _get_glyph(self, fontname, font_class, sym, fontsize, math=True):
        # Override prime symbol to use Bakoma.
        if sym == r'\prime':
            return self.bakoma._get_glyph(
                fontname, font_class, sym, fontsize, math)
        else:
            # check whether the glyph is available in the display font
            uniindex = get_unicode_index(sym)
            font = self._get_font('ex')
            if font is not None:
                glyphindex = font.get_char_index(uniindex)
                if glyphindex != 0:
                    return super()._get_glyph(
                        'ex', font_class, sym, fontsize, math)
            # otherwise return regular glyph
            return super()._get_glyph(
                fontname, font_class, sym, fontsize, math)
