    def to_period(self, freq=None, copy=True):
        """
        Convert Series from DatetimeIndex to PeriodIndex with desired
        frequency (inferred from index if not passed)

        Parameters
        ----------
        freq : string, default

        Returns
        -------
        ts : Series with PeriodIndex
        """
        new_values = self._values
        if copy:
            new_values = new_values.copy()

        new_index = self.index.to_period(freq=freq)
        return self._constructor(new_values,
                                 index=new_index).__finalize__(self)
