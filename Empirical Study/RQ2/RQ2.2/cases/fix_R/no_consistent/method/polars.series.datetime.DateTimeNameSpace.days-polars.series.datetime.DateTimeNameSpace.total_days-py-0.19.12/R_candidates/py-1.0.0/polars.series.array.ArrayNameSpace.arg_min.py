    def arg_min(self) -> Series:
        """
        Retrieve the index of the minimal value in every sub-array.

        Returns
        -------
        Series
            Series of data type :class:`UInt32` or :class:`UInt64`
            (depending on compilation).

        Examples
        --------
        >>> s = pl.Series("a", [[3, 2, 1], [9, 1, 2]], dtype=pl.Array(pl.Int64, 3))
        >>> s.arr.arg_min()
        shape: (2,)
        Series: 'a' [u32]
        [
            2
            1
        ]

        """
