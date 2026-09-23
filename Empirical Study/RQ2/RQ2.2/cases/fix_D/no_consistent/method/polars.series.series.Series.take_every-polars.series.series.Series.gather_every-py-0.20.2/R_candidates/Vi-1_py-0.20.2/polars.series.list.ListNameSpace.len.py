    def len(self) -> Series:
        """
        Return the number of elements in each list.

        Null values count towards the total.

        Returns
        -------
        Series
            Series of data type :class:`UInt32`.

        Examples
        --------
        >>> s = pl.Series([[1, 2, None], [5]])
        >>> s.list.len()
        shape: (2,)
        Series: '' [u32]
        [
            3
            1
        ]

        """
