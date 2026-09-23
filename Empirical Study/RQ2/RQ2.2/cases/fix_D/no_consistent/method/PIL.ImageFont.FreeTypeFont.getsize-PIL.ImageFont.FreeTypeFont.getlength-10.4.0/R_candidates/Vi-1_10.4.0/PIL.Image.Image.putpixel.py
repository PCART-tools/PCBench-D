    def putpixel(
        self, xy: tuple[int, int], value: float | tuple[int, ...] | list[int]
    ) -> None:
        """
        Modifies the pixel at the given position. The color is given as
        a single numerical value for single-band images, and a tuple for
        multi-band images. In addition to this, RGB and RGBA tuples are
        accepted for P and PA images.

        Note that this method is relatively slow.  For more extensive changes,
        use :py:meth:`~PIL.Image.Image.paste` or the :py:mod:`~PIL.ImageDraw`
        module instead.

        See:

        * :py:meth:`~PIL.Image.Image.paste`
        * :py:meth:`~PIL.Image.Image.putdata`
        * :py:mod:`~PIL.ImageDraw`

        :param xy: The pixel coordinate, given as (x, y). See
           :ref:`coordinate-system`.
        :param value: The pixel value.
        """

        if self.readonly:
            self._copy()
        self.load()

        if self.pyaccess:
            return self.pyaccess.putpixel(xy, value)

        if (
            self.mode in ("P", "PA")
            and isinstance(value, (list, tuple))
            and len(value) in [3, 4]
        ):
            # RGB or RGBA value for a P or PA image
            if self.mode == "PA":
                alpha = value[3] if len(value) == 4 else 255
                value = value[:3]
            palette_index = self.palette.getcolor(value, self)
            value = (palette_index, alpha) if self.mode == "PA" else palette_index
        return self.im.putpixel(xy, value)
