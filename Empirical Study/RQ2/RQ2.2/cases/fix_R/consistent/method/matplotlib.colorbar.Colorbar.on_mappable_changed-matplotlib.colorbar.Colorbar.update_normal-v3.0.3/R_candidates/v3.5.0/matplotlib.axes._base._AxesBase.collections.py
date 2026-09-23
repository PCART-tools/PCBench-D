    @property
    def collections(self):
        return self.ArtistList(self, 'collections', 'add_collection',
                               valid_types=mcoll.Collection)
