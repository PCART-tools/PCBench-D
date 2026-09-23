    @cbook.deprecated(
        "3.1", alternative="not np.isfinite(self.vertices).all()")
    @property
    def has_nonfinite(self):
        """
        `True` if the vertices array has nonfinite values.
        """
        return not np.isfinite(self._vertices).all()
