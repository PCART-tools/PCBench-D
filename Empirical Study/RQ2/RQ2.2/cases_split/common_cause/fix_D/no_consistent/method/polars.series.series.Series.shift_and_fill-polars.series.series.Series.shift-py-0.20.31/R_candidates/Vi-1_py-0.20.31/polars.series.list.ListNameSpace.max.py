    def max(self) -> Series:
        """
        Compute the max value of the arrays in the list.

        Examples
        --------
        >>> s = pl.Series("values", [[4, 1], [2, 3]])
        >>> s.list.max()
        shape: (2,)
        Series: 'values' [i64]
        [
            4
            3
        ]
        """
