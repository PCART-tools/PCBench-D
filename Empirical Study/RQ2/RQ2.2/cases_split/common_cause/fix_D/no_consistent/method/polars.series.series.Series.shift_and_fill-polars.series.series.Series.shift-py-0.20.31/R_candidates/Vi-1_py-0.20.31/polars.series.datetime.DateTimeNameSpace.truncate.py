    def truncate(
        self,
        every: str | dt.timedelta | Expr,
        offset: str | dt.timedelta | None = None,
        *,
        use_earliest: bool | None = None,
        ambiguous: Ambiguous | Series | None = None,
    ) -> Series:
        """
        Divide the date/ datetime range into buckets.

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
        offset
            Offset the window

            .. deprecated:: 0.20.19
                This argument is deprecated and will be removed in the next breaking
                release. Instead, chain `dt.truncate` with `dt.offset_by`.
        use_earliest
            Determine how to deal with ambiguous datetimes:

            - `None` (default): raise
            - `True`: use the earliest datetime
            - `False`: use the latest datetime

            .. deprecated:: 0.19.0
                This is now automatically inferred; you can safely omit this argument.
        ambiguous
            Determine how to deal with ambiguous datetimes:

            - `'raise'` (default): raise
            - `'earliest'`: use the earliest datetime
            - `'latest'`: use the latest datetime

            .. deprecated:: 0.19.3
                This is now automatically inferred; you can safely omit this argument.

        Notes
        -----
        The `every` and `offset` argument are created with the
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
        Series
            Series of data type :class:`Date` or :class:`Datetime`.

        Examples
        --------
        >>> from datetime import timedelta, datetime
        >>> s = pl.datetime_range(
        ...     datetime(2001, 1, 1),
        ...     datetime(2001, 1, 2),
        ...     timedelta(minutes=165),
        ...     eager=True,
        ... ).alias("datetime")
        >>> s
        shape: (9,)
        Series: 'datetime' [datetime[μs]]
        [
            2001-01-01 00:00:00
            2001-01-01 02:45:00
            2001-01-01 05:30:00
            2001-01-01 08:15:00
            2001-01-01 11:00:00
            2001-01-01 13:45:00
            2001-01-01 16:30:00
            2001-01-01 19:15:00
            2001-01-01 22:00:00
        ]
        >>> s.dt.truncate("1h")
        shape: (9,)
        Series: 'datetime' [datetime[μs]]
        [
            2001-01-01 00:00:00
            2001-01-01 02:00:00
            2001-01-01 05:00:00
            2001-01-01 08:00:00
            2001-01-01 11:00:00
            2001-01-01 13:00:00
            2001-01-01 16:00:00
            2001-01-01 19:00:00
            2001-01-01 22:00:00
        ]

        >>> s = pl.datetime_range(
        ...     datetime(2001, 1, 1), datetime(2001, 1, 1, 1), "10m", eager=True
        ... ).alias("datetime")
        >>> s
        shape: (7,)
        Series: 'datetime' [datetime[μs]]
        [
                2001-01-01 00:00:00
                2001-01-01 00:10:00
                2001-01-01 00:20:00
                2001-01-01 00:30:00
                2001-01-01 00:40:00
                2001-01-01 00:50:00
                2001-01-01 01:00:00
        ]
        >>> s.dt.truncate("30m")
        shape: (7,)
        Series: 'datetime' [datetime[μs]]
        [
                2001-01-01 00:00:00
                2001-01-01 00:00:00
                2001-01-01 00:00:00
                2001-01-01 00:30:00
                2001-01-01 00:30:00
                2001-01-01 00:30:00
                2001-01-01 01:00:00
        ]
        """
