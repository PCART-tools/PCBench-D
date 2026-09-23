    def minutes(self) -> Series:
        """
        Extract the minutes from a Duration type.

        Returns
        -------
        Series
            Series of data type :class:`Int64`.

        Examples
        --------
        >>> from datetime import datetime
        >>> date = pl.datetime_range(
        ...     datetime(2020, 1, 1), datetime(2020, 1, 4), "1d", eager=True
        ... )
        >>> date
        shape: (4,)
        Series: 'datetime' [datetime[μs]]
        [
                2020-01-01 00:00:00
                2020-01-02 00:00:00
                2020-01-03 00:00:00
                2020-01-04 00:00:00
        ]
        >>> date.diff().dt.minutes()
        shape: (4,)
        Series: 'datetime' [i64]
        [
                null
                1440
                1440
                1440
        ]

        """
