    @_api.deprecated("3.5")
    def get_images_artists(self):
        artists = []
        images = []

        for a in self.get_children():
            if not a.get_visible():
                continue
            if isinstance(a, mimage.AxesImage):
                images.append(a)
            else:
                artists.append(a)

        return images, artists
