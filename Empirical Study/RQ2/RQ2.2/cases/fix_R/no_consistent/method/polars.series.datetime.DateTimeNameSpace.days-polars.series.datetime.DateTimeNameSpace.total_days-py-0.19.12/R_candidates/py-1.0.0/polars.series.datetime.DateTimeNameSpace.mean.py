    @deprecate_function("Use `Series.mean` instead.", version="1.0.0")
    def mean(self) -> TemporalLiteral | None:
        """
        Return mean as python DateTime.

        .. deprecated:: 1.0.0
            Use `Series.mean` instead.

        Examples
        --------
        >>> from datetime import date, datetime
        >>> s = pl.Series([date(2001, 1, 1), date(2001, 1, 2)])
        >>> s.dt.mean()  # doctest: +SKIP
        datetime.datetime(2001, 1, 1, 12, 0)
        >>> s = pl.Series(
        ...     [datetime(2001, 1, 1), datetime(2001, 1, 2), datetime(2001, 1, 3)]
        ... )
        >>> s.dt.mean()  # doctest: +SKIP
        datetime.datetime(2001, 1, 2, 0, 0)
        """
        return self._s.mean()
