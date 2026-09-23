    def __init__(self, *args, **kwargs):
        TruetypeFonts.__init__(self, *args, **kwargs)
        self.fontmap = {}
        for key, name in self._fontmap.items():
            fullpath = findfont(name)
            self.fontmap[key] = fullpath
            self.fontmap[name] = fullpath
