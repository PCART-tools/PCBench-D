    def _sci(self, im):
        """Set the current image.

        This image will be the target of colormap functions like
        `~.pyplot.viridis`, and other functions such as `~.pyplot.clim`.  The
        current image is an attribute of the current axes.
        """
        if isinstance(im, mpl.contour.ContourSet):
            if im.collections[0] not in self.collections:
                raise ValueError("ContourSet must be in current Axes")
        elif im not in self.images and im not in self.collections:
            raise ValueError("Argument must be an image, collection, or "
                             "ContourSet in this Axes")
        self._current_image = im
