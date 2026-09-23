    def round(
        self,
        every: str | timedelta,
        offset: str | timedelta | None = None,
        *,
        ambiguous: Ambiguous | Expr | None = None,
    ) -> Expr:
        """
        Divide the date/datetime range into buckets.

        Each date/datetime in the first half of the interval
        is mapped to the start of its bucket.
        Each date/datetime in the second half of the interval
        is mapped to the end of its bucket.
        Ambiguous results are localised using the DST offset of the original timestamp -
        for example, rounding `'2022-11-06 01:20:00 CST'` by `'1h'` results in
        `'2022-11-06 01:00:00 CST'`, whereas rounding `'2022-11-06 01:20:00 CDT'` by
        `'1h'` results in `'2022-11-06 01:00:00 CDT'`.

        Parameters
        ----------
        every
            Every interval start and period length
        offset
            Offset the window
        ambiguous
            Determine how to deal with ambiguous datetimes:

            - `'raise'` (default): raise
            - `'earliest'`: use the earliest datetime
            - `'latest'`: use the latest datetime

            .. deprecated: 0.19.3
                This is now auto-inferred, you can safely remove this argument.

        Notes
        -----
        The `every` and `offset` argument are created with the
        the following small string formatting language:

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

        eg: 3d12h4m25s  # 3 days, 12 hours, 4 minutes, and 25 seconds


        By "calendar day", we mean the corresponding time on the next day (which may
        not be 24 hours, due to daylight savings). Similarly for "calendar week",
        "calendar month", "calendar quarter", and "calendar year".

        Returns
        -------
        Expr
            Expression of data type :class:`Date` or :class:`Datetime`.

        Warnings
        --------
        This functionality is currently experimental and may
        change without it being considered a breaking change.

        Examples
        --------
        >>> from datetime import timedelta, datetime
        >>> df = pl.datetime_range(
        ...     datetime(2001, 1, 1),
        ...     datetime(2001, 1, 2),
        ...     timedelta(minutes=225),
        ...     eager=True,
        ... ).to_frame()
        >>> df.with_columns(pl.col("datetime").dt.round("1h").alias("round"))
        shape: (7, 2)
        ┌─────────────────────┬─────────────────────┐
        │ datetime            ┆ round               │
        │ ---                 ┆ ---                 │
        │ datetime[μs]        ┆ datetime[μs]        │
        ╞═════════════════════╪═════════════════════╡
        │ 2001-01-01 00:00:00 ┆ 2001-01-01 00:00:00 │
        │ 2001-01-01 03:45:00 ┆ 2001-01-01 04:00:00 │
        │ 2001-01-01 07:30:00 ┆ 2001-01-01 08:00:00 │
        │ 2001-01-01 11:15:00 ┆ 2001-01-01 11:00:00 │
        │ 2001-01-01 15:00:00 ┆ 2001-01-01 15:00:00 │
        │ 2001-01-01 18:45:00 ┆ 2001-01-01 19:00:00 │
        │ 2001-01-01 22:30:00 ┆ 2001-01-01 23:00:00 │
        └─────────────────────┴─────────────────────┘

        >>> df = pl.datetime_range(
        ...     datetime(2001, 1, 1), datetime(2001, 1, 1, 1), "10m", eager=True
        ... ).to_frame()
        >>> df.with_columns(pl.col("datetime").dt.round("30m").alias("round"))
        shape: (7, 2)
        ┌─────────────────────┬─────────────────────┐
        │ datetime            ┆ round               │
        │ ---                 ┆ ---                 │
        │ datetime[μs]        ┆ datetime[μs]        │
        ╞═════════════════════╪═════════════════════╡
        │ 2001-01-01 00:00:00 ┆ 2001-01-01 00:00:00 │
        │ 2001-01-01 00:10:00 ┆ 2001-01-01 00:00:00 │
        │ 2001-01-01 00:20:00 ┆ 2001-01-01 00:30:00 │
        │ 2001-01-01 00:30:00 ┆ 2001-01-01 00:30:00 │
        │ 2001-01-01 00:40:00 ┆ 2001-01-01 00:30:00 │
        │ 2001-01-01 00:50:00 ┆ 2001-01-01 01:00:00 │
        │ 2001-01-01 01:00:00 ┆ 2001-01-01 01:00:00 │
        └─────────────────────┴─────────────────────┘

        """
        every = deprecate_saturating(every)
        offset = deprecate_saturating(offset)
        if offset is None:
            offset = "0ns"

        if ambiguous is not None:
            issue_deprecation_warning(
                "`ambiguous` is deprecated. It is now auto-inferred, you can safely remove this argument.",
                version="0.19.13",
            )

        return wrap_expr(
            self._pyexpr.dt_round(
                _timedelta_to_pl_duration(every),
                _timedelta_to_pl_duration(offset),
            )
        )
