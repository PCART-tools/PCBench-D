    def seconds(self) -> Series:
        """
        Extract the seconds from a Duration type.

        Returns
        -------
        Series
            Series of data type :class:`Int64`.

        Examples
        --------
        >>> from datetime import datetime
        >>> date = pl.datetime_range(
        ...     datetime(2020, 1, 1), datetime(2020, 1, 1, 0, 4, 0), "1m", eager=True
        ... )
        >>> date
        shape: (5,)
        Series: 'datetime' [datetime[μs]]
        [
                2020-01-01 00:00:00
                2020-01-01 00:01:00
                2020-01-01 00:02:00
                2020-01-01 00:03:00
                2020-01-01 00:04:00
        ]
        >>> date.diff().dt.seconds()
        shape: (5,)
        Series: 'datetime' [i64]
        [
                null
                60
                60
                60
                60
        ]

        """
