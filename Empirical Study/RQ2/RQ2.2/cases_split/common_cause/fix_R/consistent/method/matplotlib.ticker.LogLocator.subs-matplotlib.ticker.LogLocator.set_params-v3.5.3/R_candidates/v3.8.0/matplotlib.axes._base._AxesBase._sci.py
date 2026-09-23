    def _sci(self, im):
        """
        Set the current image.

        This image will be the target of colormap functions like
        ``pyplot.viridis``, and other functions such as `~.pyplot.clim`.  The
        current image is an attribute of the current Axes.
        """
        _api.check_isinstance((mcoll.Collection, mimage.AxesImage), im=im)
        if im not in self._children:
            raise ValueError("Argument must be an image or collection in this Axes")
        self._current_image = im
