    def set_rasterized(self, rasterized):
        """
        Force rasterized (bitmap) drawing in vector backend output.

        Defaults to None, which implies the backend's default behavior.

        Parameters
        ----------
        rasterized : bool or None
        """
        if rasterized and not hasattr(self.draw, "_supports_rasterization"):
            warnings.warn("Rasterization of '%s' will be ignored" % self)

        self._rasterized = rasterized
