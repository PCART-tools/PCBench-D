    @cache_readonly
    def _hasnans(self):
        return self._isnan.any()
