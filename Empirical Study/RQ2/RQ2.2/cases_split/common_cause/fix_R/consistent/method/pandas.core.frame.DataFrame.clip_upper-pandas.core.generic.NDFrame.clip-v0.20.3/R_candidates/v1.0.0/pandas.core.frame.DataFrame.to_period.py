    def to_period(self, freq=None, axis=0, copy=True) -> "DataFrame":
        """
        Convert DataFrame from DatetimeIndex to PeriodIndex.

        Convert DataFrame from DatetimeIndex to PeriodIndex with desired
        frequency (inferred from index if not passed).

        Parameters
        ----------
        freq : str, default
            Frequency of the PeriodIndex.
        axis : {0 or 'index', 1 or 'columns'}, default 0
            The axis to convert (the index by default).
        copy : bool, default True
            If False then underlying input data is not copied.

        Returns
        -------
        TimeSeries with PeriodIndex
        """
        new_data = self._data
        if copy:
            new_data = new_data.copy()

        axis = self._get_axis_number(axis)
        if axis == 0:
            new_data.set_axis(1, self.index.to_period(freq=freq))
        elif axis == 1:
            new_data.set_axis(0, self.columns.to_period(freq=freq))
        else:  # pragma: no cover
            raise AssertionError(f"Axis must be 0 or 1. Got {axis}")

        return self._constructor(new_data)
