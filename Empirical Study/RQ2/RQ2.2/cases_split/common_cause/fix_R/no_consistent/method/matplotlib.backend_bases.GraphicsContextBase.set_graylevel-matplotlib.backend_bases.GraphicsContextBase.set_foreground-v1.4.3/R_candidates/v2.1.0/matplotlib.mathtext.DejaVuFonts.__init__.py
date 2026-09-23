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
                 1 : 'STIXSizeOneSym',
                 2 : 'STIXSizeTwoSym',
                 3 : 'STIXSizeThreeSym',
                 4 : 'STIXSizeFourSym',
                 5 : 'STIXSizeFiveSym'})
        for key, name in six.iteritems(self._fontmap):
            fullpath = findfont(name)
            self.fontmap[key] = fullpath
            self.fontmap[name] = fullpath
