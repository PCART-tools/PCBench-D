    def __init__(self, *args, **kwargs):
        # This must come first so the backend's owner is set correctly
        if rcParams['mathtext.fallback_to_cm']:
            self.cm_fallback = BakomaFonts(*args, **kwargs)
        else:
            self.cm_fallback = None
        TruetypeFonts.__init__(self, *args, **kwargs)
        self.fontmap = {}
        for texfont in "cal rm tt it bf sf".split():
            prop = rcParams['mathtext.' + texfont]
            font = findfont(prop)
            self.fontmap[texfont] = font
        prop = FontProperties('cmex10')
        font = findfont(prop)
        self.fontmap['ex'] = font
