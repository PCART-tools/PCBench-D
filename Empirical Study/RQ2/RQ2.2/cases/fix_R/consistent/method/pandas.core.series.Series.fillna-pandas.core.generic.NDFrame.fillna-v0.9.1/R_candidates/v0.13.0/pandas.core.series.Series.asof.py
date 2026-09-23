    def asof(self, where):
        """
        Return last good (non-NaN) value in TimeSeries if value is NaN for
        requested date.

        If there is no good value, NaN is returned.

        Parameters
        ----------
        where : date or array of dates

        Notes
        -----
        Dates are assumed to be sorted

        Returns
        -------
        value or NaN
        """
        if isinstance(where, compat.string_types):
            where = datetools.to_datetime(where)

        values = self.values

        if not hasattr(where, '__iter__'):
            start = self.index[0]
            if isinstance(self.index, PeriodIndex):
                where = Period(where, freq=self.index.freq).ordinal
                start = start.ordinal

            if where < start:
                return pa.NA
            loc = self.index.searchsorted(where, side='right')
            if loc > 0:
                loc -= 1
            while isnull(values[loc]) and loc > 0:
                loc -= 1
            return values[loc]

        if not isinstance(where, Index):
            where = Index(where)

        locs = self.index.asof_locs(where, notnull(values))
        new_values = com.take_1d(values, locs)
        return self._constructor(new_values, index=where).__finalize__(self)
