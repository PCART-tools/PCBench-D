    def __init__(self, *args, **kwargs):
        TruetypeFonts.__init__(self, *args, **kwargs)
        self.fontmap = {}
        for key, name in six.iteritems(self._fontmap):
            fullpath = findfont(name)
            self.fontmap[key] = fullpath
            self.fontmap[name] = fullpath
