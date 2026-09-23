    def truncate(self, every: str | dt.timedelta | Expr) -> Expr:
        """
        Divide the date/datetime range into buckets.

        Each date/datetime is mapped to the start of its bucket using the corresponding
        local datetime. Note that weekly buckets start on Monday.
        Ambiguous results are localised using the DST offset of the original timestamp -
        for example, truncating `'2022-11-06 01:30:00 CST'` by `'1h'` results in
        `'2022-11-06 01:00:00 CST'`, whereas truncating `'2022-11-06 01:30:00 CDT'` by
        `'1h'` results in `'2022-11-06 01:00:00 CDT'`.

        Parameters
        ----------
        every
            Every interval start and period length

        Notes
        -----
        The `every` argument is created with the
        the following string language:

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

        These strings can be combined:

        - 3d12h4m25s # 3 days, 12 hours, 4 minutes, and 25 seconds


        By "calendar day", we mean the corresponding time on the next day (which may
        not be 24 hours, due to daylight savings). Similarly for "calendar week",
        "calendar month", "calendar quarter", and "calendar year".

        Returns
        -------
        Expr
            Expression of data type :class:`Date` or :class:`Datetime`.

        Examples
        --------
        >>> from datetime import timedelta, datetime
        >>> df = (
        ...     pl.datetime_range(
        ...         datetime(2001, 1, 1),
        ...         datetime(2001, 1, 2),
        ...         timedelta(minutes=225),
        ...         eager=True,
        ...     )
        ...     .alias("datetime")
        ...     .to_frame()
        ... )
        >>> df
        shape: (7, 1)
        ┌─────────────────────┐
        │ datetime            │
        │ ---                 │
        │ datetime[μs]        │
        ╞═════════════════════╡
        │ 2001-01-01 00:00:00 │
        │ 2001-01-01 03:45:00 │
        │ 2001-01-01 07:30:00 │
        │ 2001-01-01 11:15:00 │
        │ 2001-01-01 15:00:00 │
        │ 2001-01-01 18:45:00 │
        │ 2001-01-01 22:30:00 │
        └─────────────────────┘
        >>> df.select(pl.col("datetime").dt.truncate("1h"))
        shape: (7, 1)
        ┌─────────────────────┐
        │ datetime            │
        │ ---                 │
        │ datetime[μs]        │
        ╞═════════════════════╡
        │ 2001-01-01 00:00:00 │
        │ 2001-01-01 03:00:00 │
        │ 2001-01-01 07:00:00 │
        │ 2001-01-01 11:00:00 │
        │ 2001-01-01 15:00:00 │
        │ 2001-01-01 18:00:00 │
        │ 2001-01-01 22:00:00 │
        └─────────────────────┘
        >>> truncate_str = df.select(pl.col("datetime").dt.truncate("1h"))
        >>> truncate_td = df.select(pl.col("datetime").dt.truncate(timedelta(hours=1)))
        >>> truncate_str.equals(truncate_td)
        True

        >>> df = (
        ...     pl.datetime_range(
        ...         datetime(2001, 1, 1), datetime(2001, 1, 1, 1), "10m", eager=True
        ...     )
        ...     .alias("datetime")
        ...     .to_frame()
        ... )
        >>> df.select(
        ...     "datetime", pl.col("datetime").dt.truncate("30m").alias("truncate")
        ... )
        shape: (7, 2)
        ┌─────────────────────┬─────────────────────┐
        │ datetime            ┆ truncate            │
        │ ---                 ┆ ---                 │
        │ datetime[μs]        ┆ datetime[μs]        │
        ╞═════════════════════╪═════════════════════╡
        │ 2001-01-01 00:00:00 ┆ 2001-01-01 00:00:00 │
        │ 2001-01-01 00:10:00 ┆ 2001-01-01 00:00:00 │
        │ 2001-01-01 00:20:00 ┆ 2001-01-01 00:00:00 │
        │ 2001-01-01 00:30:00 ┆ 2001-01-01 00:30:00 │
        │ 2001-01-01 00:40:00 ┆ 2001-01-01 00:30:00 │
        │ 2001-01-01 00:50:00 ┆ 2001-01-01 00:30:00 │
        │ 2001-01-01 01:00:00 ┆ 2001-01-01 01:00:00 │
        └─────────────────────┴─────────────────────┘
        """
        if not isinstance(every, pl.Expr):
            every = parse_as_duration_string(every)

        every = parse_into_expression(every, str_as_lit=True)
        return wrap_expr(self._pyexpr.dt_truncate(every))
