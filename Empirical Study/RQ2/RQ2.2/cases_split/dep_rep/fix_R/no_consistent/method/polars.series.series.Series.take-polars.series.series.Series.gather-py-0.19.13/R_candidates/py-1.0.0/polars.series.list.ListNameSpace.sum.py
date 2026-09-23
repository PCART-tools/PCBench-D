    def sum(self) -> Series:
        """
        Sum all the arrays in the list.

        Examples
        --------
        >>> s = pl.Series("values", [[1], [2, 3]])
        >>> s.list.sum()
        shape: (2,)
        Series: 'values' [i64]
        [
            1
            5
        ]
        """
