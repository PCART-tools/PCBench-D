    @cache_readonly
    def is_monotonic(self):
        return self._multiindex.is_monotonic
