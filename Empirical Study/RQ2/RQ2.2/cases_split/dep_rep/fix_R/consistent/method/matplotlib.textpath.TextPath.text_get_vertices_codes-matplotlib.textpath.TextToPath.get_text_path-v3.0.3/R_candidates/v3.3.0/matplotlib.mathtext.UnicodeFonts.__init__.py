    def __init__(self, *args, **kwargs):
        # This must come first so the backend's owner is set correctly
        fallback_rc = rcParams['mathtext.fallback']
        if rcParams['mathtext.fallback_to_cm'] is not None:
            fallback_rc = ('cm' if rcParams['mathtext.fallback_to_cm']
                           else None)

        font_class = {'stix': StixFonts,
                      'stixsans': StixSansFonts,
                      'cm': BakomaFonts
                      }.get(fallback_rc)
        self.cm_fallback = font_class(*args, **kwargs) if font_class else None

        TruetypeFonts.__init__(self, *args, **kwargs)
        self.fontmap = {}
        for texfont in "cal rm tt it bf sf".split():
            prop = rcParams['mathtext.' + texfont]
            font = findfont(prop)
            self.fontmap[texfont] = font
        prop = FontProperties('cmex10')
        font = findfont(prop)
        self.fontmap['ex'] = font

        # include STIX sized alternatives for glyphs if fallback is STIX
        if isinstance(self.cm_fallback, StixFonts):
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
