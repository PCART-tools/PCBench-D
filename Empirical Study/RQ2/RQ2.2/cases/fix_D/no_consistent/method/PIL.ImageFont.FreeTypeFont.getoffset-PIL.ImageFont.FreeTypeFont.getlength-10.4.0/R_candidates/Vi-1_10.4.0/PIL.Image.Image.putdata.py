    def putdata(
        self,
        data: Sequence[float] | Sequence[Sequence[int]],
        scale: float = 1.0,
        offset: float = 0.0,
    ) -> None:
        """
        Copies pixel data from a flattened sequence object into the image. The
        values should start at the upper left corner (0, 0), continue to the
        end of the line, followed directly by the first value of the second
        line, and so on. Data will be read until either the image or the
        sequence ends. The scale and offset values are used to adjust the
        sequence values: **pixel = value*scale + offset**.

        :param data: A flattened sequence object.
        :param scale: An optional scale value.  The default is 1.0.
        :param offset: An optional offset value.  The default is 0.0.
        """

        self._ensure_mutable()

        self.im.putdata(data, scale, offset)
