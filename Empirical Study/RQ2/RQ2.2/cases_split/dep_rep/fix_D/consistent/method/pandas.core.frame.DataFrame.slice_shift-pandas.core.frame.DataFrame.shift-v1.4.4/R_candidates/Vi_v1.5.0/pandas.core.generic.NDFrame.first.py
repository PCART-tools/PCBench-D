    @final
    def first(self: NDFrameT, offset) -> NDFrameT:
        """
        Select initial periods of time series data based on a date offset.

        When having a DataFrame with dates as index, this function can
        select the first few rows based on a date offset.

        Parameters
        ----------
        offset : str, DateOffset or dateutil.relativedelta
            The offset length of the data that will be selected. For instance,
            '1M' will display all the rows having their index within the first month.

        Returns
        -------
        Series or DataFrame
            A subset of the caller.

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
        >>> ts = pd.DataFrame({'A': [1, 2, 3, 4]}, index=i)
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

        Notice the data for 3 first calendar days were returned, not the first
        3 days observed in the dataset, and therefore data for 2018-04-13 was
        not returned.
        """
        if not isinstance(self.index, DatetimeIndex):
            raise TypeError("'first' only supports a DatetimeIndex index")

        if len(self.index) == 0:
            return self

        offset = to_offset(offset)
        if not isinstance(offset, Tick) and offset.is_on_offset(self.index[0]):
            # GH#29623 if first value is end of period, remove offset with n = 1
            #  before adding the real offset
            end_date = end = self.index[0] - offset.base + offset
        else:
            end_date = end = self.index[0] + offset

        # Tick-like, e.g. 3 weeks
        if isinstance(offset, Tick) and end_date in self.index:
            end = self.index.searchsorted(end_date, side="left")
            return self.iloc[:end]

        return self.loc[:end]
