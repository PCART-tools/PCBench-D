    @cache_readonly
    def mid(self):
        """
        Return the midpoint of each Interval in the IntervalIndex as an Index
        """
        return self._data.mid
