    def first(self: FrameOrSeries, offset) -> FrameOrSeries:
        """
        Method to subset initial periods of time series data based on a date offset.

        Parameters
        ----------
        offset : str, DateOffset, dateutil.relativedelta

        Returns
        -------
        subset : same type as caller

        Raises
        ------
        TypeError
            If the index is not  a :class:`DatetimeIndex`

        See Also
        --------
        last : Select final periods of time series based on a date offset.
        at_time : Select values at a particular time of the day.
        between_time : Select values between particular times of the day.

        Examples
        --------
        >>> i = pd.date_range('2018-04-09', periods=4, freq='2D')
        >>> ts = pd.DataFrame({'A': [1,2,3,4]}, index=i)
        >>> ts
                    A
        2018-04-09  1
        2018-04-11  2
        2018-04-13  3
        2018-04-15  4

        Get the rows for the first 3 days:

        >>> ts.first('3D')
                    A
        2018-04-09  1
        2018-04-11  2

        Notice the data for 3 first calender days were returned, not the first
        3 days observed in the dataset, and therefore data for 2018-04-13 was
        not returned.
        """
        if not isinstance(self.index, DatetimeIndex):
            raise TypeError("'first' only supports a DatetimeIndex index")

        if len(self.index) == 0:
            return self

        offset = to_offset(offset)
        end_date = end = self.index[0] + offset

        # Tick-like, e.g. 3 weeks
        if not offset.is_anchored() and hasattr(offset, "_inc"):
            if end_date in self.index:
                end = self.index.searchsorted(end_date, side="left")
                return self.iloc[:end]

        return self.loc[:end]
