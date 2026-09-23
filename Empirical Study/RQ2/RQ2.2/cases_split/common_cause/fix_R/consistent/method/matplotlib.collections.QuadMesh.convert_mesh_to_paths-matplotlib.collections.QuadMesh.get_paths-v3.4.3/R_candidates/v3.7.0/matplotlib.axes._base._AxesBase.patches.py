    @property
    def patches(self):
        return self.ArtistList(self, 'patches', valid_types=mpatches.Patch)
