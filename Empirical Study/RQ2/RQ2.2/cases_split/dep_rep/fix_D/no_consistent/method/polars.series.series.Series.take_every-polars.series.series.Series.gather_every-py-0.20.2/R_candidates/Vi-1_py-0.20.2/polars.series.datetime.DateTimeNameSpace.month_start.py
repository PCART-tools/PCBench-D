    def month_start(self) -> Series:
        """
        Roll backward to the first day of the month.

        Returns
        -------
        Series
            Series of data type :class:`Date` or :class:`Datetime`.

        Notes
        -----
        If you're coming from pandas, you can think of this as a vectorised version
        of `pandas.tseries.offsets.MonthBegin().rollback(datetime)`.

        Examples
        --------
        >>> from datetime import datetime
        >>> s = pl.datetime_range(
        ...     datetime(2000, 1, 2, 2), datetime(2000, 4, 2, 2), "1mo", eager=True
        ... )
        >>> s.dt.month_start()
        shape: (4,)
        Series: 'datetime' [datetime[μs]]
        [
                2000-01-01 02:00:00
                2000-02-01 02:00:00
                2000-03-01 02:00:00
                2000-04-01 02:00:00
        ]
        """
