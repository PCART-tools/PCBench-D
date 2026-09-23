    def to_list(self) -> Series:
        """
        Convert an Array column into a List column with the same inner data type.

        Returns
        -------
        Series
            Series of data type :class:`List`.

        Examples
        --------
        >>> s = pl.Series([[1, 2], [3, 4]], dtype=pl.Array(pl.Int8, 2))
        >>> s.arr.to_list()
        shape: (2,)
        Series: '' [list[i8]]
        [
                [1, 2]
                [3, 4]
        ]
        """
