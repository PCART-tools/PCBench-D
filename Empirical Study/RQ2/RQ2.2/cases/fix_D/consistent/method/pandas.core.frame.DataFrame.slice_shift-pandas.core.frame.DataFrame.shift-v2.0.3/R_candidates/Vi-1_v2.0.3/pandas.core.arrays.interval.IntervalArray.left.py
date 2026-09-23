    @property
    def left(self):
        """
        Return the left endpoints of each Interval in the IntervalArray as an Index.
        """
        from pandas import Index

        return Index(self._left, copy=False)
