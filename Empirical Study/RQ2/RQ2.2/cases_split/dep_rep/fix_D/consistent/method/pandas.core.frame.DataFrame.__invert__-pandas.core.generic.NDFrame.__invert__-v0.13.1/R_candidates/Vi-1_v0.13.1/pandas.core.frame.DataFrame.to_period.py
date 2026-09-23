    def to_period(self, freq=None, axis=0, copy=True):
        """
        Convert DataFrame from DatetimeIndex to PeriodIndex with desired
        frequency (inferred from index if not passed)

        Parameters
        ----------
        freq : string, default
        axis : {0, 1}, default 0
            The axis to convert (the index by default)
        copy : boolean, default True
            If False then underlying input data is not copied

        Returns
        -------
        ts : TimeSeries with PeriodIndex
        """
        new_data = self._data
        if copy:
            new_data = new_data.copy()

        axis = self._get_axis_number(axis)
        if axis == 0:
            if freq is None:
                freq = self.index.freqstr or self.index.inferred_freq
            new_data.set_axis(1, self.index.to_period(freq=freq))
        elif axis == 1:
            if freq is None:
                freq = self.columns.freqstr or self.columns.inferred_freq
            new_data.set_axis(0, self.columns.to_period(freq=freq))
        else:  # pragma: no cover
            raise AssertionError('Axis must be 0 or 1. Got %s' % str(axis))

        return self._constructor(new_data)
