    @cbook.deprecated("3.0")
    @property
    def afmfiles(self):
        return [font.fname for font in self.afmlist]
