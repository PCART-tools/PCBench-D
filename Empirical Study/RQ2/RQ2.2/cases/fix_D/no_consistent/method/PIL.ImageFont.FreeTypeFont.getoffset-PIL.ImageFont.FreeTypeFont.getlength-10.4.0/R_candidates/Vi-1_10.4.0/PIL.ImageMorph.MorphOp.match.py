    def match(self, image: Image.Image) -> list[tuple[int, int]]:
        """Get a list of coordinates matching the morphological operation on
        an image.

        Returns a list of tuples of (x,y) coordinates
        of all matching pixels. See :ref:`coordinate-system`."""
        if self.lut is None:
            msg = "No operator loaded"
            raise Exception(msg)

        if image.mode != "L":
            msg = "Image mode must be L"
            raise ValueError(msg)
        return _imagingmorph.match(bytes(self.lut), image.im.id)
