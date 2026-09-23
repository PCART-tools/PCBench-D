    def __init__(self, *args, **kwargs):
        self._stix_fallback = StixFonts(*args, **kwargs)

        TruetypeFonts.__init__(self, *args, **kwargs)
        self.fontmap = {}
        for key, val in self._fontmap.items():
            fullpath = findfont(val)
            self.fontmap[key] = fullpath
            self.fontmap[val] = fullpath
