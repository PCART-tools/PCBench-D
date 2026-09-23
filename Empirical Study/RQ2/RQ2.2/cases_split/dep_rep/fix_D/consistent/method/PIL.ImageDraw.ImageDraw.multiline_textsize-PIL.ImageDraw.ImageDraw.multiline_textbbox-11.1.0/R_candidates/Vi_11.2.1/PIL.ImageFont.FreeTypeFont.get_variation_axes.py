    def get_variation_axes(self) -> list[Axis]:
        """
        :returns: A list of the axes in a variation font.
        :exception OSError: If the font is not a variation font.
        """
        try:
            axes = self.font.getvaraxes()
        except AttributeError as e:
            msg = "FreeType 2.9.1 or greater is required"
            raise NotImplementedError(msg) from e
        for axis in axes:
            if axis["name"]:
                axis["name"] = axis["name"].replace(b"\x00", b"")
        return axes
