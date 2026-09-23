    def total_nanoseconds(self) -> Series:
        """
        Extract the total nanoseconds from a Duration type.

        Returns
        -------
        Series
            Series of data type :class:`Int64`.

        Examples
        --------
        >>> from datetime import datetime
        >>> date = pl.datetime_range(
        ...     datetime(2020, 1, 1),
        ...     datetime(2020, 1, 1, 0, 0, 1, 0),
        ...     "1ms",
        ...     eager=True,
        ... ).alias("datetime")[:3]
        >>> date
        shape: (3,)
        Series: 'datetime' [datetime[μs]]
        [
                2020-01-01 00:00:00
                2020-01-01 00:00:00.001
                2020-01-01 00:00:00.002
        ]
        >>> date.diff().dt.total_nanoseconds()
        shape: (3,)
        Series: 'datetime' [i64]
        [
                null
                1000000
                1000000
        ]
        """
