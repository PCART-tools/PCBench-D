    @cache_readonly
    def is_monotonic_increasing(self):
        return self._multiindex.is_monotonic_increasing
