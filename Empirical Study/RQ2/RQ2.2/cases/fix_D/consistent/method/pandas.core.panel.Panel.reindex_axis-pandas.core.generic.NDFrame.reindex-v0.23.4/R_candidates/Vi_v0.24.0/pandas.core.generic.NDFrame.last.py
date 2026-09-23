    def last(self, offset):
        """
        Convenience method for subsetting final periods of time series data
        based on a date offset.

        Parameters
        ----------
        offset : string, DateOffset, dateutil.relativedelta

        Returns
        -------
        subset : same type as caller

        Raises
        ------
        TypeError
            If the index is not  a :class:`DatetimeIndex`

        See Also
        --------
        first : Select initial periods of time series based on a date offset.
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

        Get the rows for the last 3 days:

        >>> ts.last('3D')
                    A
        2018-04-13  3
        2018-04-15  4

        Notice the data for 3 last calender days were returned, not the last
        3 observed days in the dataset, and therefore data for 2018-04-11 was
        not returned.
        """
        if not isinstance(self.index, DatetimeIndex):
            raise TypeError("'last' only supports a DatetimeIndex index")

        if len(self.index) == 0:
            return self

        offset = to_offset(offset)

        start_date = self.index[-1] - offset
        start = self.index.searchsorted(start_date, side='right')
        return self.iloc[start:]
