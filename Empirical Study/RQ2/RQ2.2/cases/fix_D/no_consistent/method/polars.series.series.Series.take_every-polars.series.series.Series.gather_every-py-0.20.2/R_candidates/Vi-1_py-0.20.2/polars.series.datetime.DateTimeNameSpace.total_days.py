    def total_days(self) -> Series:
        """
        Extract the total days from a Duration type.

        Returns
        -------
        Series
            Series of data type :class:`Int64`.

        Examples
        --------
        >>> from datetime import datetime
        >>> date = pl.datetime_range(
        ...     datetime(2020, 3, 1), datetime(2020, 5, 1), "1mo", eager=True
        ... )
        >>> date
        shape: (3,)
        Series: 'datetime' [datetime[μs]]
        [
                2020-03-01 00:00:00
                2020-04-01 00:00:00
                2020-05-01 00:00:00
        ]
        >>> date.diff().dt.total_days()
        shape: (3,)
        Series: 'datetime' [i64]
        [
                null
                31
                30
        ]

        """
