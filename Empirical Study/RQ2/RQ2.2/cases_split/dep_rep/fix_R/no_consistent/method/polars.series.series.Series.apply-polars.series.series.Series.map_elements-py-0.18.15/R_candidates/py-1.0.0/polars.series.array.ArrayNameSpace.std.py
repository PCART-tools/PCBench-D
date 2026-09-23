    def std(self, ddof: int = 1) -> Series:
        """
        Compute the std of the values of the sub-arrays.

        Examples
        --------
        >>> s = pl.Series("a", [[1, 2], [4, 3]], dtype=pl.Array(pl.Int64, 2))
        >>> s.arr.std()
        shape: (2,)
        Series: 'a' [f64]
        [
            0.707107
            0.707107
        ]
        """
