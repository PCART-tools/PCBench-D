    def is_leap_year(self) -> Series:
        """
        Determine whether the year of the underlying date representation is a leap year.

        Applies to Date and Datetime columns.

        Returns
        -------
        Series
            Series of data type :class:`Boolean`.

        Examples
        --------
        >>> from datetime import date
        >>> s = pl.Series(
        ...     "date", [date(2000, 1, 1), date(2001, 1, 1), date(2002, 1, 1)]
        ... )
        >>> s.dt.is_leap_year()
        shape: (3,)
        Series: 'date' [bool]
        [
                true
                false
                false
        ]

        """
