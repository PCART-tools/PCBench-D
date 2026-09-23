    def _sci(self, im):
        """
        Set the current image.

        This image will be the target of colormap functions like
        `~.pyplot.viridis`, and other functions such as `~.pyplot.clim`.  The
        current image is an attribute of the current Axes.
        """
        _api.check_isinstance(
            (mpl.contour.ContourSet, mcoll.Collection, mimage.AxesImage),
            im=im)
        if isinstance(im, mpl.contour.ContourSet):
            if im.collections[0] not in self._children:
                raise ValueError("ContourSet must be in current Axes")
        elif im not in self._children:
            raise ValueError("Argument must be an image, collection, or "
                             "ContourSet in this Axes")
        self._current_image = im
