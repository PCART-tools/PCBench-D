    def dst_offset(self) -> Series:
        """
        Additional offset currently in effect (typically due to daylight saving time).

        Returns
        -------
        Series
            Series of data type :class:`Duration`.

        See Also
        --------
        Series.dt.base_utc_offset : Base offset from UTC.

        Examples
        --------
        >>> from datetime import datetime
        >>> s = pl.datetime_range(
        ...     datetime(2020, 10, 25),
        ...     datetime(2020, 10, 26),
        ...     time_zone="Europe/London",
        ...     eager=True,
        ... ).alias("datetime")
        >>> s
        shape: (2,)
        Series: 'datetime' [datetime[μs, Europe/London]]
        [
                2020-10-25 00:00:00 BST
                2020-10-26 00:00:00 GMT
        ]
        >>> s.dt.dst_offset()
        shape: (2,)
        Series: 'datetime' [duration[ms]]
        [
                1h
                0ms
        ]
        """
