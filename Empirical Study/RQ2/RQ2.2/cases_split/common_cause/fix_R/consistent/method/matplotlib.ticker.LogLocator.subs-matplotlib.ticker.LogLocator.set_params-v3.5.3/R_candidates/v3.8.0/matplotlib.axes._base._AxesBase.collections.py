    @property
    def collections(self):
        return self.ArtistList(self, 'collections',
                               valid_types=mcoll.Collection)
