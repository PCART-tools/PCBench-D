    def weekday(self) -> Series:
        """
        Extract the week day from the underlying date representation.

        Applies to Date and Datetime columns.

        Returns the ISO weekday number where monday = 1 and sunday = 7

        Returns
        -------
        Series
            Series of data type :class:`Int8`.

        Examples
        --------
        >>> from datetime import date
        >>> s = pl.date_range(date(2001, 1, 1), date(2001, 1, 7), eager=True)
        >>> s.dt.weekday()
        shape: (7,)
        Series: 'date' [i8]
        [
                1
                2
                3
                4
                5
                6
                7
        ]

        """
