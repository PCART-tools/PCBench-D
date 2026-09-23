    def __getitem__(self, xy: tuple[int, int] | list[int]) -> float | tuple[int, ...]:
        """
        Returns the pixel at x,y. The pixel is returned as a single
        value for single band images or a tuple for multiple band
        images

        :param xy: The pixel coordinate, given as (x, y). See
          :ref:`coordinate-system`.
        :returns: a pixel value for single band images, a tuple of
          pixel values for multiband images.
        """
        (x, y) = xy
        if x < 0:
            x = self.xsize + x
        if y < 0:
            y = self.ysize + y
        (x, y) = self.check_xy((x, y))
        return self.get_pixel(x, y)
