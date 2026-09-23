    def at_time(
        self: FrameOrSeries, time, asof: bool_t = False, axis=None
    ) -> FrameOrSeries:
        """
        Select values at particular time of day (e.g. 9:30AM).

        Parameters
        ----------
        time : datetime.time or str
        axis : {0 or 'index', 1 or 'columns'}, default 0

            .. versionadded:: 0.24.0

        Returns
        -------
        Series or DataFrame

        Raises
        ------
        TypeError
            If the index is not  a :class:`DatetimeIndex`

        See Also
        --------
        between_time : Select values between particular times of the day.
        first : Select initial periods of time series based on a date offset.
        last : Select final periods of time series based on a date offset.
        DatetimeIndex.indexer_at_time : Get just the index locations for
            values at particular time of the day.

        Examples
        --------
        >>> i = pd.date_range('2018-04-09', periods=4, freq='12H')
        >>> ts = pd.DataFrame({'A': [1, 2, 3, 4]}, index=i)
        >>> ts
                             A
        2018-04-09 00:00:00  1
        2018-04-09 12:00:00  2
        2018-04-10 00:00:00  3
        2018-04-10 12:00:00  4

        >>> ts.at_time('12:00')
                             A
        2018-04-09 12:00:00  2
        2018-04-10 12:00:00  4
        """
        if axis is None:
            axis = self._stat_axis_number
        axis = self._get_axis_number(axis)

        index = self._get_axis(axis)
        try:
            indexer = index.indexer_at_time(time, asof=asof)
        except AttributeError:
            raise TypeError("Index must be DatetimeIndex")

        return self._take_with_is_copy(indexer, axis=axis)
