    @property
    def lines(self):
        return self.ArtistList(self, 'lines', 'add_line',
                               valid_types=mlines.Line2D)
