    def microsecond(self) -> Series:
        """
        Extract the microseconds from the underlying DateTime representation.

        Applies to Datetime columns.

        Returns
        -------
        Series
            Series of data type :class:`Int32`.

        Examples
        --------
        >>> from datetime import datetime
        >>> start = datetime(2001, 1, 1)
        >>> stop = datetime(2001, 1, 1, 0, 0, 4)
        >>> date = pl.datetime_range(start, stop, interval="500ms", eager=True)
        >>> date
        shape: (9,)
        Series: 'datetime' [datetime[μs]]
        [
                2001-01-01 00:00:00
                2001-01-01 00:00:00.500
                2001-01-01 00:00:01
                2001-01-01 00:00:01.500
                2001-01-01 00:00:02
                2001-01-01 00:00:02.500
                2001-01-01 00:00:03
                2001-01-01 00:00:03.500
                2001-01-01 00:00:04
        ]
        >>> date.dt.microsecond()
        shape: (9,)
        Series: 'datetime' [i32]
        [
                0
                500000
                0
                500000
                0
                500000
                0
                500000
                0
        ]

        """
