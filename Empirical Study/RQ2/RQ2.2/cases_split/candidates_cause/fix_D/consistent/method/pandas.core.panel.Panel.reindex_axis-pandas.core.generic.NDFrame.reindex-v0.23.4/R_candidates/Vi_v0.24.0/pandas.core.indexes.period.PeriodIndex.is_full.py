    @property
    def is_full(self):
        """
        Returns True if this PeriodIndex is range-like in that all Periods
        between start and end are present, in order.
        """
        if len(self) == 0:
            return True
        if not self.is_monotonic:
            raise ValueError('Index is not monotonic')
        values = self.asi8
        return ((values[1:] - values[:-1]) < 2).all()
