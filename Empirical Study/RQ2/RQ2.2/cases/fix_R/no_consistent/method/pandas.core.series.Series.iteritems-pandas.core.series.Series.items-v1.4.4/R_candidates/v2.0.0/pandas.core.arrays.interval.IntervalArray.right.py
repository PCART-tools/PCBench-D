    @property
    def right(self):
        """
        Return the right endpoints of each Interval in the IntervalArray as an Index.
        """
        from pandas import Index

        return Index(self._right, copy=False)
