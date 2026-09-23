    def add_image(self, image):
        """
        Add an `~.AxesImage` to the axes' images; return the image.
        """
        self._set_artist_props(image)
        if not image.get_label():
            image.set_label('_image%d' % len(self.images))
        self.images.append(image)
        image._remove_method = self.images.remove
        self.stale = True
        return image
