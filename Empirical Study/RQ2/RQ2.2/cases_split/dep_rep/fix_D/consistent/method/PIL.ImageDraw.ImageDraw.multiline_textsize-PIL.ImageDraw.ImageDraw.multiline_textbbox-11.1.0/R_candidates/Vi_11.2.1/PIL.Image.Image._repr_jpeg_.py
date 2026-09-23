    def _repr_jpeg_(self) -> bytes | None:
        """iPython display hook support for JPEG format.

        :returns: JPEG version of the image as bytes
        """
        return self._repr_image("JPEG")
