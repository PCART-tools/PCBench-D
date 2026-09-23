    def between_time(self, start_time, end_time, include_start=True,
                     include_end=True):
        """
        Select values between particular times of the day (e.g., 9:00-9:30 AM).

        By setting ``start_time`` to be later than ``end_time``,
        you can get the times that are *not* between the two times.

        Raises
        ------
        TypeError
            If the index is not  a :class:`DatetimeIndex`

        Parameters
        ----------
        start_time : datetime.time or string
        end_time : datetime.time or string
        include_start : boolean, default True
        include_end : boolean, default True

        Returns
        -------
        values_between_time : type of caller

        Examples
        --------
        >>> i = pd.date_range('2018-04-09', periods=4, freq='1D20min')
        >>> ts = pd.DataFrame({'A': [1,2,3,4]}, index=i)
        >>> ts
                             A
        2018-04-09 00:00:00  1
        2018-04-10 00:20:00  2
        2018-04-11 00:40:00  3
        2018-04-12 01:00:00  4

        >>> ts.between_time('0:15', '0:45')
                             A
        2018-04-10 00:20:00  2
        2018-04-11 00:40:00  3

        You get the times that are *not* between two times by setting
        ``start_time`` later than ``end_time``:

        >>> ts.between_time('0:45', '0:15')
                             A
        2018-04-09 00:00:00  1
        2018-04-12 01:00:00  4

        See Also
        --------
        at_time : Select values at a particular time of the day
        first : Select initial periods of time series based on a date offset
        last : Select final periods of time series based on a date offset
        DatetimeIndex.indexer_between_time : Get just the index locations for
            values between particular times of the day
        """
        try:
            indexer = self.index.indexer_between_time(
                start_time, end_time, include_start=include_start,
                include_end=include_end)
            return self._take(indexer)
        except AttributeError:
            raise TypeError('Index must be DatetimeIndex')
