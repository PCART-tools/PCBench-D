    def sum(self) -> Series:
        """
        Compute the sum values of the sub-arrays.

        Examples
        --------
        >>> s = pl.Series([[1, 2], [4, 3]], dtype=pl.Array(pl.Int64, 2))
        >>> s.arr.sum()
        shape: (2,)
        Series: '' [i64]
        [
            3
            7
        ]
        """
