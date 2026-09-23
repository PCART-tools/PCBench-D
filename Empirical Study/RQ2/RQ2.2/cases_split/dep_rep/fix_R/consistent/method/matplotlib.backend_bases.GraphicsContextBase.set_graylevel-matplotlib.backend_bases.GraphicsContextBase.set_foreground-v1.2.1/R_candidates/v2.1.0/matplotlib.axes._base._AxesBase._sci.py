    def _sci(self, im):
        """
        helper for :func:`~matplotlib.pyplot.sci`;
        do not use elsewhere.
        """
        if isinstance(im, matplotlib.contour.ContourSet):
            if im.collections[0] not in self.collections:
                raise ValueError(
                    "ContourSet must be in current Axes")
        elif im not in self.images and im not in self.collections:
            raise ValueError(
                "Argument must be an image, collection, or ContourSet in "
                "this Axes")
        self._current_image = im
