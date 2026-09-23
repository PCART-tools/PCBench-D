    def minute(self) -> Series:
        """
        Extract the minutes from the underlying DateTime representation.

        Applies to Datetime columns.

        Returns the minute number from 0 to 59.

        Returns
        -------
        Series
            Series of data type :class:`Int8`.

        Examples
        --------
        >>> from datetime import datetime
        >>> start = datetime(2001, 1, 1)
        >>> stop = datetime(2001, 1, 1, 0, 4, 0)
        >>> date = pl.datetime_range(start, stop, interval="2m", eager=True)
        >>> date
        shape: (3,)
        Series: 'datetime' [datetime[μs]]
        [
                2001-01-01 00:00:00
                2001-01-01 00:02:00
                2001-01-01 00:04:00
        ]
        >>> date.dt.minute()
        shape: (3,)
        Series: 'datetime' [i8]
        [
                0
                2
                4
        ]

        """
