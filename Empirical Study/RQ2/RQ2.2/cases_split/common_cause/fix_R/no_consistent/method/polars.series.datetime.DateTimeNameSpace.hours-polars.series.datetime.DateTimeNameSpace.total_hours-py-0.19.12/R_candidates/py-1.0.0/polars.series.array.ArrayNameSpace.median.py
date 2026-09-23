    def median(self) -> Series:
        """
        Compute the median of the values of the sub-arrays.

        Examples
        --------
        >>> s = pl.Series("a", [[1, 2], [4, 3]], dtype=pl.Array(pl.Int64, 2))
        >>> s.arr.median()
        shape: (2,)
        Series: 'a' [f64]
        [
            1.5
            3.5
        ]
        """
