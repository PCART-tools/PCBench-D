    @deprecate_function("Use `Series.median` instead.", version="1.0.0")
    def median(self) -> TemporalLiteral | None:
        """
        Return median as python DateTime.

        .. deprecated:: 1.0.0
            Use `Series.median` instead.

        Examples
        --------
        >>> from datetime import date, datetime
        >>> s = pl.Series([date(2001, 1, 1), date(2001, 1, 2)])
        >>> s.dt.median()  # doctest: +SKIP
        datetime.datetime(2001, 1, 1, 12, 0)
        >>> date = pl.datetime_range(
        ...     datetime(2001, 1, 1), datetime(2001, 1, 3), "1d", eager=True
        ... ).alias("datetime")
        >>> date
        shape: (3,)
        Series: 'datetime' [datetime[μs]]
        [
                2001-01-01 00:00:00
                2001-01-02 00:00:00
                2001-01-03 00:00:00
        ]
        >>> date.dt.median()  # doctest: +SKIP
        datetime.datetime(2001, 1, 2, 0, 0)
        """
        return self._s.median()
