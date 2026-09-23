    def reduce(
        self,
        factor: int | tuple[int, int],
        box: tuple[int, int, int, int] | None = None,
    ) -> Image:
        """
        Returns a copy of the image reduced ``factor`` times.
        If the size of the image is not dividable by ``factor``,
        the resulting size will be rounded up.

        :param factor: A greater than 0 integer or tuple of two integers
           for width and height separately.
        :param box: An optional 4-tuple of ints providing
           the source image region to be reduced.
           The values must be within ``(0, 0, width, height)`` rectangle.
           If omitted or ``None``, the entire source is used.
        """
        if not isinstance(factor, (list, tuple)):
            factor = (factor, factor)

        if box is None:
            box = (0, 0) + self.size

        if factor == (1, 1) and box == (0, 0) + self.size:
            return self.copy()

        if self.mode in ["LA", "RGBA"]:
            im = self.convert({"LA": "La", "RGBA": "RGBa"}[self.mode])
            im = im.reduce(factor, box)
            return im.convert(self.mode)

        self.load()

        return self._new(self.im.reduce(factor, box))
