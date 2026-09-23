    @property
    def length(self):
        """
        Return an Index with entries denoting the length of each Interval in
        the IntervalIndex
        """
        return self._data.length
