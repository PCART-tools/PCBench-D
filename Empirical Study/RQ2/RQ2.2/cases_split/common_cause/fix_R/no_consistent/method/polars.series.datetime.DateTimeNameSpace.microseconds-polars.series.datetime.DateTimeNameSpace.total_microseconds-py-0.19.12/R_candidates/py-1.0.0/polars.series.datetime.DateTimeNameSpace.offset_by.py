    def offset_by(self, by: str | Expr) -> Series:
        """
        Offset this date by a relative time offset.

        This differs from `pl.col("foo") + timedelta` in that it can
        take months and leap years into account. Note that only a single minus
        sign is allowed in the `by` string, as the first character.

        Parameters
        ----------
        by
            The offset is dictated by the following string language:

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

            By "calendar day", we mean the corresponding time on the next day
            (which may not be 24 hours, due to daylight savings). Similarly for
            "calendar week", "calendar month", "calendar quarter", and
            "calendar year".

        Returns
        -------
        Series
            Series of data type :class:`Date` or :class:`Datetime`.

        Examples
        --------
        >>> from datetime import datetime
        >>> dates = pl.datetime_range(
        ...     datetime(2000, 1, 1), datetime(2005, 1, 1), "1y", eager=True
        ... ).alias("datetime")
        >>> dates
        shape: (6,)
        Series: 'datetime' [datetime[μs]]
        [
                2000-01-01 00:00:00
                2001-01-01 00:00:00
                2002-01-01 00:00:00
                2003-01-01 00:00:00
                2004-01-01 00:00:00
                2005-01-01 00:00:00
        ]
        >>> dates.dt.offset_by("1y").alias("date_plus_1y")
        shape: (6,)
        Series: 'date_plus_1y' [datetime[μs]]
        [
                2001-01-01 00:00:00
                2002-01-01 00:00:00
                2003-01-01 00:00:00
                2004-01-01 00:00:00
                2005-01-01 00:00:00
                2006-01-01 00:00:00
        ]
        >>> dates.dt.offset_by("-1y2mo").alias("date_minus_1y_2mon")
        shape: (6,)
        Series: 'date_minus_1y_2mon' [datetime[μs]]
        [
                1998-11-01 00:00:00
                1999-11-01 00:00:00
                2000-11-01 00:00:00
                2001-11-01 00:00:00
                2002-11-01 00:00:00
                2003-11-01 00:00:00
        ]
        """
