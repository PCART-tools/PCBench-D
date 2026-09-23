    def var(self, ddof: int = 1) -> Series:
        """
        Compute the var of the values of the sub-arrays.

        Examples
        --------
        >>> s = pl.Series("a", [[1, 2], [4, 3]], dtype=pl.Array(pl.Int64, 2))
        >>> s.arr.var()
        shape: (2,)
        Series: 'a' [f64]
        [
                0.5
                0.5
        ]
        """
