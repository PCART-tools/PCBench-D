    @cache_readonly
    def is_monotonic_increasing(self) -> bool:
        """
        Return True if the IntervalIndex is monotonic increasing (only equal or
        increasing values), else False
        """
        return self._engine.is_monotonic_increasing
