    def getextrema(self) -> tuple[float, float] | tuple[tuple[int, int], ...]:
        """
        Gets the minimum and maximum pixel values for each band in
        the image.

        :returns: For a single-band image, a 2-tuple containing the
           minimum and maximum pixel value.  For a multi-band image,
           a tuple containing one 2-tuple for each band.
        """

        self.load()
        if self.im.bands > 1:
            return tuple(self.im.getband(i).getextrema() for i in range(self.im.bands))
        return self.im.getextrema()
