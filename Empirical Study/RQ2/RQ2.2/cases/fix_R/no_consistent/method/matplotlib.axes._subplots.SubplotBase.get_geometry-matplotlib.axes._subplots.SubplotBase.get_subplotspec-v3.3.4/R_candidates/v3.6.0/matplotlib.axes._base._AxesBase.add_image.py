    def add_image(self, image):
        """
        Add an `.AxesImage` to the Axes; return the image.
        """
        self._deprecate_noninstance('add_image', mimage.AxesImage, image=image)
        self._set_artist_props(image)
        if not image.get_label():
            image.set_label(f'_child{len(self._children)}')
        self._children.append(image)
        image._remove_method = self._children.remove
        self.stale = True
        return image
