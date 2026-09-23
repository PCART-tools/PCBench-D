    @property
    def tables(self):
        return self.ArtistList(self, 'tables', valid_types=mtable.Table)
