    def _repr_png_(self) -> bytes | None:
        """iPython display hook support for PNG format.

        :returns: PNG version of the image as bytes
        """
        return self._repr_image("PNG", compress_level=1)
