    def hour(self) -> Series:
        """
        Extract the hour from the underlying DateTime representation.

        Applies to Datetime columns.

        Returns the hour number from 0 to 23.

        Returns
        -------
        Series
            Series of data type :class:`Int8`.

        Examples
        --------
        >>> from datetime import datetime
        >>> start = datetime(2001, 1, 1)
        >>> stop = datetime(2001, 1, 1, 3)
        >>> date = pl.datetime_range(start, stop, interval="1h", eager=True)
        >>> date
        shape: (4,)
        Series: 'datetime' [datetime[μs]]
        [
                2001-01-01 00:00:00
                2001-01-01 01:00:00
                2001-01-01 02:00:00
                2001-01-01 03:00:00
        ]
        >>> date.dt.hour()
        shape: (4,)
        Series: 'datetime' [i8]
        [
                0
                1
                2
                3
        ]

        """
