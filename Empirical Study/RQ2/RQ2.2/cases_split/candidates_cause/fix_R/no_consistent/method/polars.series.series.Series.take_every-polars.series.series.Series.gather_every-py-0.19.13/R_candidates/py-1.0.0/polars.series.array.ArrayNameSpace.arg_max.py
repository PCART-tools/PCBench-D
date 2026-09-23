    def arg_max(self) -> Series:
        """
        Retrieve the index of the maximum value in every sub-array.

        Returns
        -------
        Series
            Series of data type :class:`UInt32` or :class:`UInt64`
            (depending on compilation).

        Examples
        --------
        >>> s = pl.Series("a", [[0, 9, 3], [9, 1, 2]], dtype=pl.Array(pl.Int64, 3))
        >>> s.arr.arg_max()
        shape: (2,)
        Series: 'a' [u32]
        [
            1
            0
        ]

        """
