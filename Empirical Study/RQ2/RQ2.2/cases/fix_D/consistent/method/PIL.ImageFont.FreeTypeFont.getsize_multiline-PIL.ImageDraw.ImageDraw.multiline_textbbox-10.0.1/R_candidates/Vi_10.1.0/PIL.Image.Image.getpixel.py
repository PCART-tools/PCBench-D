    def getpixel(self, xy):
        """
        Returns the pixel value at a given position.

        :param xy: The coordinate, given as (x, y). See
           :ref:`coordinate-system`.
        :returns: The pixel value.  If the image is a multi-layer image,
           this method returns a tuple.
        """

        self.load()
        if self.pyaccess:
            return self.pyaccess.getpixel(xy)
        return self.im.getpixel(tuple(xy))
