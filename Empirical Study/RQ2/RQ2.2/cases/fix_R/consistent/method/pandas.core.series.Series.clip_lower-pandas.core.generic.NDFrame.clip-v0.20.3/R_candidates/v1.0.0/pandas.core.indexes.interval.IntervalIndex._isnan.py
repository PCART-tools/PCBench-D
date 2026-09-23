    @cache_readonly
    def _isnan(self):
        """
        Return a mask indicating if each value is NA.
        """
        if self._mask is None:
            self._mask = isna(self.left)
        return self._mask
