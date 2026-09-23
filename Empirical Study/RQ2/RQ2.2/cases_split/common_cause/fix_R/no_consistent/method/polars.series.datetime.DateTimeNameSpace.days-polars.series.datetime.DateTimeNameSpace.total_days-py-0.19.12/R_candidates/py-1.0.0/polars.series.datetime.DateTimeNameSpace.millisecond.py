    def millisecond(self) -> Series:
        """
        Extract the milliseconds from the underlying DateTime representation.

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
        >>> s = pl.datetime_range(start, stop, interval="500ms", eager=True).alias(
        ...     "datetime"
        ... )
        >>> s.dt.millisecond()
        shape: (9,)
        Series: 'datetime' [i32]
        [
                0
                500
                0
                500
                0
                500
                0
                500
                0
        ]
        """
