    def set_variation_by_axes(self, axes: list[float]) -> None:
        """
        :param axes: A list of values for each axis.
        :exception OSError: If the font is not a variation font.
        """
        try:
            self.font.setvaraxes(axes)
        except AttributeError as e:
            msg = "FreeType 2.9.1 or greater is required"
            raise NotImplementedError(msg) from e
