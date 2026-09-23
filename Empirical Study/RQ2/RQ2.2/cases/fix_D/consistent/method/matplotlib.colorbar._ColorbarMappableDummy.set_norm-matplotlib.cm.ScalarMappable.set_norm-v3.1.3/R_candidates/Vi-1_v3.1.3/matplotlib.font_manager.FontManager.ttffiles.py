    @cbook.deprecated("3.0")
    @property
    def ttffiles(self):
        return [font.fname for font in self.ttflist]
