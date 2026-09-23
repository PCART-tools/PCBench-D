    @property
    def tables(self):
        return self.ArtistList(self, 'tables', 'add_table',
                               valid_types=mtable.Table)
