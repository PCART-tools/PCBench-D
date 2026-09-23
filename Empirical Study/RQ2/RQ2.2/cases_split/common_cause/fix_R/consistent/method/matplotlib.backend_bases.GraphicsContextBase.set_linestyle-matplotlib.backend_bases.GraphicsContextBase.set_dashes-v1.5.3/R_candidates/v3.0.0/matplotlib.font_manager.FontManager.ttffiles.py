    @property
    @cbook.deprecated("3.0")
    def ttffiles(self):
        return [font.fname for font in self.ttflist]
