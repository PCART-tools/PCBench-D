    def set_params(self, base):
        """Set parameters within this locator."""
        if base is not None:
            self._edge = _Edge_integer(base, 0)
