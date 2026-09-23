    def sort(self, *, descending: bool = False) -> Series:
        """
        Sort the arrays in this column.

        Parameters
        ----------
        descending
            Sort in descending order.

        Examples
        --------
        >>> s = pl.Series("a", [[3, 2, 1], [9, 1, 2]])
        >>> s.list.sort()
        shape: (2,)
        Series: 'a' [list[i64]]
        [
                [1, 2, 3]
                [1, 2, 9]
        ]
        >>> s.list.sort(descending=True)
        shape: (2,)
        Series: 'a' [list[i64]]
        [
                [3, 2, 1]
                [9, 2, 1]
        ]

        """
