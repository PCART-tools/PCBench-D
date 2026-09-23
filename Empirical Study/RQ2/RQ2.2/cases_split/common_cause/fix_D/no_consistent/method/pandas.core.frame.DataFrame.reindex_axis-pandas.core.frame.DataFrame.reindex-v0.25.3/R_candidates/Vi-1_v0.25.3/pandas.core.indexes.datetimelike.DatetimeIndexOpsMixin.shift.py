    @deprecate_kwarg(old_arg_name="n", new_arg_name="periods")
    def shift(self, periods, freq=None):
        """
        Shift index by desired number of time frequency increments.

        This method is for shifting the values of datetime-like indexes
        by a specified time increment a given number of times.

        Parameters
        ----------
        periods : int
            Number of periods (or increments) to shift by,
            can be positive or negative.

            .. versionchanged:: 0.24.0

        freq : pandas.DateOffset, pandas.Timedelta or string, optional
            Frequency increment to shift by.
            If None, the index is shifted by its own `freq` attribute.
            Offset aliases are valid strings, e.g., 'D', 'W', 'M' etc.

        Returns
        -------
        pandas.DatetimeIndex
            Shifted index.

        See Also
        --------
        Index.shift : Shift values of Index.
        PeriodIndex.shift : Shift values of PeriodIndex.
        """
        result = self._data._time_shift(periods, freq=freq)
        return type(self)(result, name=self.name)
