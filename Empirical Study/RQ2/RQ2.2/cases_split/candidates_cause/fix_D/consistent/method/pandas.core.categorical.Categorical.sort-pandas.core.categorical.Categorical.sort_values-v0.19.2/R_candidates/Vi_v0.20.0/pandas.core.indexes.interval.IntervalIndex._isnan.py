    @cache_readonly
    def _isnan(self):
        """ return if each value is nan"""
        if self._mask is None:
            self._mask = isnull(self.left)
        return self._mask
