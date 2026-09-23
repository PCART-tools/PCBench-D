    def iso_year(self) -> Series:
        """
        Extract ISO year from underlying Date representation.

        Applies to Date and Datetime columns.

        Returns the year number according to the ISO standard.
        This may not correspond with the calendar year.

        Returns
        -------
        Series
            Series of data type :class:`Int32`.

        Examples
        --------
        >>> from datetime import datetime
        >>> dt = datetime(2022, 1, 1, 7, 8, 40)
        >>> pl.Series([dt]).dt.iso_year()
        shape: (1,)
        Series: '' [i32]
        [
                2021
        ]

        """
