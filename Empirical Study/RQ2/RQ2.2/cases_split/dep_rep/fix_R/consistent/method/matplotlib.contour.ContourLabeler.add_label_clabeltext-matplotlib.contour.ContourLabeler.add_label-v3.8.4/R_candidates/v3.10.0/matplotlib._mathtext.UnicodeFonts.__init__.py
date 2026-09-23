    def __init__(self, default_font_prop: FontProperties, load_glyph_flags: LoadFlags):
        # This must come first so the backend's owner is set correctly
        fallback_rc = mpl.rcParams['mathtext.fallback']
        font_cls: type[TruetypeFonts] | None = {
            'stix': StixFonts,
            'stixsans': StixSansFonts,
            'cm': BakomaFonts
        }.get(fallback_rc)
        self._fallback_font = (font_cls(default_font_prop, load_glyph_flags)
                               if font_cls else None)

        super().__init__(default_font_prop, load_glyph_flags)
        for texfont in "cal rm tt it bf sf bfit".split():
            prop = mpl.rcParams['mathtext.' + texfont]
            font = findfont(prop)
            self.fontmap[texfont] = font
        prop = FontProperties('cmex10')
        font = findfont(prop)
        self.fontmap['ex'] = font

        # include STIX sized alternatives for glyphs if fallback is STIX
        if isinstance(self._fallback_font, StixFonts):
            stixsizedaltfonts = {
                 0: 'STIXGeneral',
                 1: 'STIXSizeOneSym',
                 2: 'STIXSizeTwoSym',
                 3: 'STIXSizeThreeSym',
                 4: 'STIXSizeFourSym',
                 5: 'STIXSizeFiveSym'}

            for size, name in stixsizedaltfonts.items():
                fullpath = findfont(name)
                self.fontmap[size] = fullpath
                self.fontmap[name] = fullpath
