    @cache_readonly
    def is_monotonic(self) -> bool:
        """
        Return True if the IntervalIndex is monotonic increasing (only equal or
        increasing values), else False
        """
        return self.is_monotonic_increasing
