    def day(self) -> Series:
        """
        Extract the day from the underlying date representation.

        Applies to Date and Datetime columns.

        Returns the day of month starting from 1.
        The return value ranges from 1 to 31. (The last day of month differs by months.)

        Returns
        -------
        Series
            Series of data type :class:`Int8`.

        Examples
        --------
        >>> from datetime import date
        >>> s = pl.date_range(
        ...     date(2001, 1, 1), date(2001, 1, 9), interval="2d", eager=True
        ... ).alias("date")
        >>> s.dt.day()
        shape: (5,)
        Series: 'date' [i8]
        [
                1
                3
                5
                7
                9
        ]
        """
