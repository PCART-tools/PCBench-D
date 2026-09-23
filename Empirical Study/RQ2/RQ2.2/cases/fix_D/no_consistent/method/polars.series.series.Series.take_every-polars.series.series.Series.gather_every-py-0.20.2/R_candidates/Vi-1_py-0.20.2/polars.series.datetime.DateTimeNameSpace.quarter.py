    def quarter(self) -> Series:
        """
        Extract quarter from underlying Date representation.

        Applies to Date and Datetime columns.

        Returns the quarter ranging from 1 to 4.

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
        >>> date.dt.quarter()
        shape: (4,)
        Series: 'date' [i8]
        [
                1
                1
                1
                2
        ]

        """
