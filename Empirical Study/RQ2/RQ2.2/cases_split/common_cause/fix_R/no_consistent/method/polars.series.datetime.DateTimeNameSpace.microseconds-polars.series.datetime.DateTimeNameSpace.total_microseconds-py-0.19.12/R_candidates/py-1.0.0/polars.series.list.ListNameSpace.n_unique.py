    def n_unique(self) -> Series:
        """
        Count the number of unique values in every sub-lists.

        Examples
        --------
        >>> s = pl.Series("a", [[1, 1, 2], [2, 3, 4]])
        >>> s.list.n_unique()
        shape: (2,)
        Series: 'a' [u32]
        [
            2
            3
        ]
        """
