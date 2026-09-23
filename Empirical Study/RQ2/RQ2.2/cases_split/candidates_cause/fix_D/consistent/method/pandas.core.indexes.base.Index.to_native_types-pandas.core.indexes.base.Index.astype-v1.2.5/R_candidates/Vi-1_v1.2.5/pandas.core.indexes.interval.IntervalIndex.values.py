    @cache_readonly
    def values(self) -> IntervalArray:
        """
        Return the IntervalIndex's data as an IntervalArray.
        """
        return self._data
