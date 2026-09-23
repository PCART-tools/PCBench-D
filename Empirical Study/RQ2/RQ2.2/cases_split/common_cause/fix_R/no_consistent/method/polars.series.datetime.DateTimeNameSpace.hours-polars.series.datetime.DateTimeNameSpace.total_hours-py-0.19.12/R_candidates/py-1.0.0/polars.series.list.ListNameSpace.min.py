    def min(self) -> Series:
        """
        Compute the min value of the arrays in the list.

        Examples
        --------
        >>> s = pl.Series("values", [[4, 1], [2, 3]])
        >>> s.list.min()
        shape: (2,)
        Series: 'values' [i64]
        [
            1
            2
        ]
        """
