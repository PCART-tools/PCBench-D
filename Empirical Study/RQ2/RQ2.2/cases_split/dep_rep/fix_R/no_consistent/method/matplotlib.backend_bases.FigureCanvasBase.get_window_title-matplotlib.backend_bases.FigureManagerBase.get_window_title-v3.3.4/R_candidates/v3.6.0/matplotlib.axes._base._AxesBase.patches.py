    @property
    def patches(self):
        return self.ArtistList(self, 'patches', 'add_patch',
                               valid_types=mpatches.Patch)
