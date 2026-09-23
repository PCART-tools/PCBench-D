    def round(
        self,
        every: str | dt.timedelta,
        offset: str | dt.timedelta | None = None,
        *,
        ambiguous: Ambiguous | Series | None = None,
    ) -> Series:
        """
        Divide the date/ datetime range into buckets.

        Each date/datetime in the first half of the interval
        is mapped to the start of its bucket.
        Each date/datetime in the second half of the interval
        is mapped to the end of its bucket.
        Ambiguous results are localised using the DST offset of the original timestamp -
        for example, rounding `'2022-11-06 01:20:00 CST'` by `'1h'` results in
        `'2022-11-06 01:00:00 CST'`, whereas rounding `'2022-11-06 01:20:00 CDT'` by
        `'1h'` results in `'2022-11-06 01:00:00 CDT'`.

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

            .. deprecated:: 0.19.3
                This is now auto-inferred, you can safely remove this argument.

        Returns
        -------
        Series
            Series of data type :class:`Date` or :class:`Datetime`.

        Warnings
        --------
        This functionality is currently experimental and may
        change without it being considered a breaking change.

        Examples
        --------
        >>> from datetime import timedelta, datetime
        >>> start = datetime(2001, 1, 1)
        >>> stop = datetime(2001, 1, 2)
        >>> s = pl.datetime_range(
        ...     start, stop, timedelta(minutes=165), eager=True
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
        >>> s.dt.round("1h")
        shape: (9,)
        Series: 'datetime' [datetime[μs]]
        [
            2001-01-01 00:00:00
            2001-01-01 03:00:00
            2001-01-01 06:00:00
            2001-01-01 08:00:00
            2001-01-01 11:00:00
            2001-01-01 14:00:00
            2001-01-01 17:00:00
            2001-01-01 19:00:00
            2001-01-01 22:00:00
        ]
        >>> round_str = s.dt.round("1h")
        >>> round_td = s.dt.round(timedelta(hours=1))
        >>> round_str.equals(round_td)
        True

        >>> start = datetime(2001, 1, 1)
        >>> stop = datetime(2001, 1, 1, 1)
        >>> s = pl.datetime_range(start, stop, "10m", eager=True).alias("datetime")
        >>> s.dt.round("30m")
        shape: (7,)
        Series: 'datetime' [datetime[μs]]
        [
                2001-01-01 00:00:00
                2001-01-01 00:00:00
                2001-01-01 00:30:00
                2001-01-01 00:30:00
                2001-01-01 00:30:00
                2001-01-01 01:00:00
                2001-01-01 01:00:00
        ]
        """
