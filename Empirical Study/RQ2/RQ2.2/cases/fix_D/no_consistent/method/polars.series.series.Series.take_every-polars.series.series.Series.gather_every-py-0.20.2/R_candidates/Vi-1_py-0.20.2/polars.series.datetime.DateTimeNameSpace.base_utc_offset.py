    def base_utc_offset(self) -> Series:
        """
        Base offset from UTC.

        This is usually constant for all datetimes in a given time zone, but
        may vary in the rare case that a country switches time zone, like
        Samoa (Apia) did at the end of 2011.

        Returns
        -------
        Series
            Series of data type :class:`Duration`.

        See Also
        --------
        Series.dt.dst_offset : Additional offset currently in effect.

        Examples
        --------
        >>> from datetime import datetime
        >>> s = pl.datetime_range(
        ...     datetime(2011, 12, 29),
        ...     datetime(2012, 1, 1),
        ...     "2d",
        ...     time_zone="Pacific/Apia",
        ...     eager=True,
        ... )
        >>> s
        shape: (2,)
        Series: 'datetime' [datetime[μs, Pacific/Apia]]
        [
                2011-12-29 00:00:00 -10
                2011-12-31 00:00:00 +14
        ]
        >>> s.dt.base_utc_offset()
        shape: (2,)
        Series: 'datetime' [duration[ms]]
        [
                -11h
                13h
        ]
        """
