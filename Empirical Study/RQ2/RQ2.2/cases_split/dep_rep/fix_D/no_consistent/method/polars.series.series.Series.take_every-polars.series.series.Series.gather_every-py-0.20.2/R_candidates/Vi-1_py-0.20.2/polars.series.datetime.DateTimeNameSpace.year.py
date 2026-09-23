    def year(self) -> Series:
        """
        Extract the year from the underlying date representation.

        Applies to Date and Datetime columns.

        Returns the year number in the calendar date.

        Returns
        -------
        Series
            Series of data type :class:`Int32`.

        Examples
        --------
        >>> from datetime import date
        >>> s = pl.Series("date", [date(2001, 1, 1), date(2002, 1, 1)])
        >>> s.dt.year()
        shape: (2,)
        Series: 'date' [i32]
        [
                2001
                2002
        ]

        """
