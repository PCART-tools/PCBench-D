    def __setitem__(self, xy, color):
        """
        Modifies the pixel at x,y. The color is given as a single
        numerical value for single band images, and a tuple for
        multi-band images

        :param xy: The pixel coordinate, given as (x, y). See
           :ref:`coordinate-system`.
        :param color: The pixel value.
        """
        if self.readonly:
            msg = "Attempt to putpixel a read only image"
            raise ValueError(msg)
        (x, y) = xy
        if x < 0:
            x = self.xsize + x
        if y < 0:
            y = self.ysize + y
        (x, y) = self.check_xy((x, y))

        if (
            self._im.mode in ("P", "PA")
            and isinstance(color, (list, tuple))
            and len(color) in [3, 4]
        ):
            # RGB or RGBA value for a P or PA image
            if self._im.mode == "PA":
                alpha = color[3] if len(color) == 4 else 255
                color = color[:3]
            color = self._palette.getcolor(color, self._img)
            if self._im.mode == "PA":
                color = (color, alpha)

        return self.set_pixel(x, y, color)
