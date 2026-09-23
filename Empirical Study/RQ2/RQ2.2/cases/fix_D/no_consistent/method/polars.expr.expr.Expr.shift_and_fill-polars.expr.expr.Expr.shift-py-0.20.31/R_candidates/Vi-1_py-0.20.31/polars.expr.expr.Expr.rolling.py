    def rolling(
        self,
        index_column: str,
        *,
        period: str | timedelta,
        offset: str | timedelta | None = None,
        closed: ClosedInterval = "right",
        check_sorted: bool | None = None,
    ) -> Self:
        """
        Create rolling groups based on a temporal or integer column.

        If you have a time series `<t_0, t_1, ..., t_n>`, then by default the
        windows created will be

            * (t_0 - period, t_0]
            * (t_1 - period, t_1]
            * ...
            * (t_n - period, t_n]

        whereas if you pass a non-default `offset`, then the windows will be

            * (t_0 + offset, t_0 + offset + period]
            * (t_1 + offset, t_1 + offset + period]
            * ...
            * (t_n + offset, t_n + offset + period]

        The `period` and `offset` arguments are created either from a timedelta, or
        by using the following string language:

        - 1ns   (1 nanosecond)
        - 1us   (1 microsecond)
        - 1ms   (1 millisecond)
        - 1s    (1 second)
        - 1m    (1 minute)
        - 1h    (1 hour)
        - 1d    (1 calendar day)
        - 1w    (1 calendar week)
        - 1mo   (1 calendar month)
        - 1q    (1 calendar quarter)
        - 1y    (1 calendar year)
        - 1i    (1 index count)

        Or combine them:
        "3d12h4m25s" # 3 days, 12 hours, 4 minutes, and 25 seconds

        By "calendar day", we mean the corresponding time on the next day (which may
        not be 24 hours, due to daylight savings). Similarly for "calendar week",
        "calendar month", "calendar quarter", and "calendar year".

        Parameters
        ----------
        index_column
            Column used to group based on the time window.
            Often of type Date/Datetime.
            This column must be sorted in ascending order.
            In case of a rolling group by on indices, dtype needs to be one of
            {UInt32, UInt64, Int32, Int64}. Note that the first three get temporarily
            cast to Int64, so if performance matters use an Int64 column.
        period
            Length of the window - must be non-negative.
        offset
            Offset of the window. Default is `-period`.
        closed : {'right', 'left', 'both', 'none'}
            Define which sides of the temporal interval are closed (inclusive).
        check_sorted
            Whether to check that `index_column` is sorted.
            If you are sure the data is sorted, you can set this to `False`.
            Doing so incorrectly will lead to incorrect output.

        Examples
        --------
        >>> dates = [
        ...     "2020-01-01 13:45:48",
        ...     "2020-01-01 16:42:13",
        ...     "2020-01-01 16:45:09",
        ...     "2020-01-02 18:12:48",
        ...     "2020-01-03 19:45:32",
        ...     "2020-01-08 23:16:43",
        ... ]
        >>> df = pl.DataFrame({"dt": dates, "a": [3, 7, 5, 9, 2, 1]}).with_columns(
        ...     pl.col("dt").str.strptime(pl.Datetime).set_sorted()
        ... )
        >>> df.with_columns(
        ...     sum_a=pl.sum("a").rolling(index_column="dt", period="2d"),
        ...     min_a=pl.min("a").rolling(index_column="dt", period="2d"),
        ...     max_a=pl.max("a").rolling(index_column="dt", period="2d"),
        ... )
        shape: (6, 5)
        ┌─────────────────────┬─────┬───────┬───────┬───────┐
        │ dt                  ┆ a   ┆ sum_a ┆ min_a ┆ max_a │
        │ ---                 ┆ --- ┆ ---   ┆ ---   ┆ ---   │
        │ datetime[μs]        ┆ i64 ┆ i64   ┆ i64   ┆ i64   │
        ╞═════════════════════╪═════╪═══════╪═══════╪═══════╡
        │ 2020-01-01 13:45:48 ┆ 3   ┆ 3     ┆ 3     ┆ 3     │
        │ 2020-01-01 16:42:13 ┆ 7   ┆ 10    ┆ 3     ┆ 7     │
        │ 2020-01-01 16:45:09 ┆ 5   ┆ 15    ┆ 3     ┆ 7     │
        │ 2020-01-02 18:12:48 ┆ 9   ┆ 24    ┆ 3     ┆ 9     │
        │ 2020-01-03 19:45:32 ┆ 2   ┆ 11    ┆ 2     ┆ 9     │
        │ 2020-01-08 23:16:43 ┆ 1   ┆ 1     ┆ 1     ┆ 1     │
        └─────────────────────┴─────┴───────┴───────┴───────┘
        """
        period = deprecate_saturating(period)
        offset = deprecate_saturating(offset)
        if offset is None:
            offset = negate_duration_string(parse_as_duration_string(period))

        period = parse_as_duration_string(period)
        offset = parse_as_duration_string(offset)

        return self._from_pyexpr(
            self._pyexpr.rolling(index_column, period, offset, closed)
        )
