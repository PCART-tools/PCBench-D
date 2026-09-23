    @property
    @cbook.deprecated("3.0")
    def afmfiles(self):
        return [font.fname for font in self.afmlist]
