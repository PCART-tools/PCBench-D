    def ordinal_day(self) -> Series:
        """
        Extract ordinal day from underlying date representation.

        Applies to Date and Datetime columns.

        Returns the day of year starting from 1.
        The return value ranges from 1 to 366. (The last day of year differs by years.)

        Returns
        -------
        Series
            Series of data type :class:`Int16`.

        Examples
        --------
        >>> from datetime import date
        >>> s = pl.date_range(
        ...     date(2001, 1, 1), date(2001, 3, 1), interval="1mo", eager=True
        ... )
        >>> s.dt.ordinal_day()
        shape: (3,)
        Series: 'date' [i16]
        [
                1
                32
                60
        ]

        """
