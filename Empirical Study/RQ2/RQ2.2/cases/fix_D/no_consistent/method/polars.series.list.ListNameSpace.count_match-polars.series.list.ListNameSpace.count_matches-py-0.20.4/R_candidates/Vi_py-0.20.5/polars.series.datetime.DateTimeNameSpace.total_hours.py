    def total_hours(self) -> Series:
        """
        Extract the total hours from a Duration type.

        Returns
        -------
        Series
            Series of data type :class:`Int64`.

        Examples
        --------
        >>> from datetime import datetime
        >>> date = pl.datetime_range(
        ...     datetime(2020, 1, 1), datetime(2020, 1, 4), "1d", eager=True
        ... ).alias("datetime")
        >>> date
        shape: (4,)
        Series: 'datetime' [datetime[μs]]
        [
                2020-01-01 00:00:00
                2020-01-02 00:00:00
                2020-01-03 00:00:00
                2020-01-04 00:00:00
        ]
        >>> date.diff().dt.total_hours()
        shape: (4,)
        Series: 'datetime' [i64]
        [
                null
                24
                24
                24
        ]
        """
