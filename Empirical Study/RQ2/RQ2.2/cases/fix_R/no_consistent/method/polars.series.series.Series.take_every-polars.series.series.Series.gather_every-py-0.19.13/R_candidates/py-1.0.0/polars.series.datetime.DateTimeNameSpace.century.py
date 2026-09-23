    def century(self) -> Expr:
        """
        Extract the century from underlying representation.

        Applies to Date and Datetime columns.

        Returns the century number in the calendar date.

        Returns
        -------
        Expr
            Expression of data type :class:`Int32`.

        Examples
        --------
        >>> from datetime import date
        >>> s = pl.Series(
        ...     "dt",
        ...     [
        ...         date(999, 12, 31),
        ...         date(1897, 5, 7),
        ...         date(2000, 1, 1),
        ...         date(2001, 7, 5),
        ...         date(3002, 10, 20),
        ...     ],
        ... )
        >>> s.dt.century()
        shape: (5,)
        Series: 'dt' [i32]
        [
            10
            19
            20
            21
            31
        ]
        """
