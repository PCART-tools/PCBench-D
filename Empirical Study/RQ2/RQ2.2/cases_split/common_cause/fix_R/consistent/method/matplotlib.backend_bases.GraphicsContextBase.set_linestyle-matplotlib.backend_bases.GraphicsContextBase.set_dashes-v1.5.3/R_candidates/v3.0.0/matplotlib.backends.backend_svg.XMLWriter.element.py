    def element(self, tag, text=None, attrib={}, **extra):
        self.start(*(tag, attrib), **extra)
        if text:
            self.data(text)
        self.end(indent=False)
