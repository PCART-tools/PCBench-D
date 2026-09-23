    def arg_min(self) -> Series:
        """
        Retrieve the index of the minimal value in every sublist.

        Returns
        -------
        Series
            Series of data type :class:`UInt32` or :class:`UInt64`
            (depending on compilation).

        Examples
        --------
        >>> s = pl.Series("a", [[1, 2], [2, 1]])
        >>> s.list.arg_min()
        shape: (2,)
        Series: 'a' [u32]
        [
            0
            1
        ]
        """
