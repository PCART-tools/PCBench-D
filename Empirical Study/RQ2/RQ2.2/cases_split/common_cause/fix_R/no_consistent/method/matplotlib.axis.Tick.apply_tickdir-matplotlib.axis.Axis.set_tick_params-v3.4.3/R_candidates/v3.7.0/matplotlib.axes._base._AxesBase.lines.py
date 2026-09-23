    @property
    def lines(self):
        return self.ArtistList(self, 'lines', valid_types=mlines.Line2D)
