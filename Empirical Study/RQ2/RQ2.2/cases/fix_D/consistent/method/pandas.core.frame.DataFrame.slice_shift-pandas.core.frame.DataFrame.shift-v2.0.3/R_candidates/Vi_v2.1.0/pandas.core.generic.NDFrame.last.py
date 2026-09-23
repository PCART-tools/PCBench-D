    @final
    def last(self, offset) -> Self:
        """
        Select final periods of time series data based on a date offset.

        For a DataFrame with a sorted DatetimeIndex, this function
        selects the last few rows based on a date offset.

        Parameters
        ----------
        offset : str, DateOffset, dateutil.relativedelta
            The offset length of the data that will be selected. For instance,
            '3D' will display all the rows having their index within the last 3 days.

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
        first : Select initial periods of time series based on a date offset.
        at_time : Select values at a particular time of the day.
        between_time : Select values between particular times of the day.

        Notes
        -----
        .. deprecated:: 2.1.0
            Please create a mask and filter using `.loc` instead

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

        Get the rows for the last 3 days:

        >>> ts.last('3D') # doctest: +SKIP
                    A
        2018-04-13  3
        2018-04-15  4

        Notice the data for 3 last calendar days were returned, not the last
        3 observed days in the dataset, and therefore data for 2018-04-11 was
        not returned.
        """
        warnings.warn(
            "last is deprecated and will be removed in a future version. "
            "Please create a mask and filter using `.loc` instead",
            FutureWarning,
            stacklevel=find_stack_level(),
        )

        if not isinstance(self.index, DatetimeIndex):
            raise TypeError("'last' only supports a DatetimeIndex index")

        if len(self.index) == 0:
            return self.copy(deep=False)

        offset = to_offset(offset)

        start_date = self.index[-1] - offset
        start = self.index.searchsorted(start_date, side="right")
        return self.iloc[start:]
