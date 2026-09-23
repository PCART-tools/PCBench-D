    @property
    def images(self):
        return self.ArtistList(self, 'images', valid_types=mimage.AxesImage)
