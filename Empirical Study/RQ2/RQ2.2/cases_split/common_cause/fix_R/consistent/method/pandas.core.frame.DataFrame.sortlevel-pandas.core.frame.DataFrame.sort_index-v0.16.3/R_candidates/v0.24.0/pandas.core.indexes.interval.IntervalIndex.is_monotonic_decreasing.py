    @cache_readonly
    def is_monotonic_decreasing(self):
        """
        Return True if the IntervalIndex is monotonic decreasing (only equal or
        decreasing values), else False
        """
        return self._multiindex.is_monotonic_decreasing
