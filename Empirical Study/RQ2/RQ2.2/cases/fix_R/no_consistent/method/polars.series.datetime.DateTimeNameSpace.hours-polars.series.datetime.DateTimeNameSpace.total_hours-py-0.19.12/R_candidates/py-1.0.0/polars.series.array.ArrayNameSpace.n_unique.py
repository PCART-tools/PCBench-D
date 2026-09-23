    def n_unique(self) -> Series:
        """
        Count the number of unique values in every sub-arrays.

        Examples
        --------
        >>> s = pl.Series("a", [[1, 2], [4, 4]], dtype=pl.Array(pl.Int64, 2))
        >>> s.arr.n_unique()
        shape: (2,)
        Series: 'a' [u32]
        [
            2
            1
        ]
        """
