    @property
    def left(self):
        """
        Return the left endpoints of each Interval in the IntervalIndex as
        an Index
        """
        return self._data._left
