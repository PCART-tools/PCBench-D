    def get_xydata(self):
        """Return the *xy* data as a (N, 2) array."""
        if self._invalidy or self._invalidx:
            self.recache()
        return self._xy
