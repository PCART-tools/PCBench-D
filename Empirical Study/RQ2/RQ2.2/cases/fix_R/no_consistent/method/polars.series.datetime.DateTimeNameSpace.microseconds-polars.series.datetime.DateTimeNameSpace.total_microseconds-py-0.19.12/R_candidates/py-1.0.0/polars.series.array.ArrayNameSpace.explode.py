    def explode(self) -> Series:
        """
        Returns a column with a separate row for every array element.

        Returns
        -------
        Series
            Series with the data type of the array elements.

        Examples
        --------
        >>> s = pl.Series("a", [[1, 2, 3], [4, 5, 6]], dtype=pl.Array(pl.Int64, 3))
        >>> s.arr.explode()
        shape: (6,)
        Series: 'a' [i64]
        [
            1
            2
            3
            4
            5
            6
        ]
        """
