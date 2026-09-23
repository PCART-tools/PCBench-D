    def reverse(self) -> Series:
        """
        Reverse the arrays in this column.

        Examples
        --------
        >>> s = pl.Series("a", [[3, 2, 1], [9, 1, 2]], dtype=pl.Array(pl.Int64, 3))
        >>> s.arr.reverse()
        shape: (2,)
        Series: 'a' [array[i64, 3]]
        [
            [1, 2, 3]
            [2, 1, 9]
        ]

        """
