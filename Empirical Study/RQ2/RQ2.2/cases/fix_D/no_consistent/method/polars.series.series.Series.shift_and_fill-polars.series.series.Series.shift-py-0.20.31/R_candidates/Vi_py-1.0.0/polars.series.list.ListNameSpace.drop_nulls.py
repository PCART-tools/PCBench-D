    def drop_nulls(self) -> Series:
        """
        Drop all null values in the list.

        The original order of the remaining elements is preserved.

        Examples
        --------
        >>> s = pl.Series("values", [[None, 1, None, 2], [None], [3, 4]])
        >>> s.list.drop_nulls()
        shape: (3,)
        Series: 'values' [list[i64]]
        [
            [1, 2]
            []
            [3, 4]
        ]
        """
