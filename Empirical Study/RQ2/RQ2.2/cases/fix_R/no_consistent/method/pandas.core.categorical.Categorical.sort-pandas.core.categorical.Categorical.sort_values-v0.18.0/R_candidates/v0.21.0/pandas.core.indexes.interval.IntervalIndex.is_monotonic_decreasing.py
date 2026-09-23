    @cache_readonly
    def is_monotonic_decreasing(self):
        return self._multiindex.is_monotonic_decreasing
