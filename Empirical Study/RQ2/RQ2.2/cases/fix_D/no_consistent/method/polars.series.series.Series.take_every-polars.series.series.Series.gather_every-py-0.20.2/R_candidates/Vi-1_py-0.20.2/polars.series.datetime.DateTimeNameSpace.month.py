    def month(self) -> Series:
        """
        Extract the month from the underlying date representation.

        Applies to Date and Datetime columns.

        Returns the month number starting from 1.
        The return value ranges from 1 to 12.

        Returns
        -------
        Series
            Series of data type :class:`Int8`.

        Examples
        --------
        >>> from datetime import date
        >>> date = pl.date_range(
        ...     date(2001, 1, 1), date(2001, 4, 1), interval="1mo", eager=True
        ... )
        >>> date.dt.month()
        shape: (4,)
        Series: 'date' [i8]
        [
                1
                2
                3
                4
        ]

        """
