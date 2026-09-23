    @property
    def images(self):
        return self.ArtistList(self, 'images', 'add_image',
                               valid_types=mimage.AxesImage)
