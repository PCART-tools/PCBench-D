    @cache_readonly
    def values(self):
        """
        Return the IntervalIndex's data as an IntervalArray.
        """
        return self._data
