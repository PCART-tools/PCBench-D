    @cache_readonly
    def hasnans(self):
        return self._isnan.any()
