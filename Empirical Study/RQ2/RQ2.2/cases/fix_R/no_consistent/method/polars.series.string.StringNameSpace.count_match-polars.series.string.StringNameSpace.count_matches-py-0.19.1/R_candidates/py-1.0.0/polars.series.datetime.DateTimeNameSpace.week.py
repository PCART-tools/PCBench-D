    def week(self) -> Series:
        """
        Extract the week from the underlying date representation.

        Applies to Date and Datetime columns.

        Returns the ISO week number starting from 1.
        The return value ranges from 1 to 53. (The last week of year differs by years.)

        Returns
        -------
        Series
            Series of data type :class:`Int8`.

        Examples
        --------
        >>> from datetime import date
        >>> date = pl.date_range(
        ...     date(2001, 1, 1), date(2001, 4, 1), interval="1mo", eager=True
        ... ).alias("date")
        >>> date.dt.week()
        shape: (4,)
        Series: 'date' [i8]
        [
                1
                5
                9
                13
        ]
        """
