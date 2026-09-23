    def reverse(self) -> Series:
        """
        Reverse the arrays in the list.

        Examples
        --------
        >>> s = pl.Series("a", [[3, 2, 1], [9, 1, 2]])
        >>> s.list.reverse()
        shape: (2,)
        Series: 'a' [list[i64]]
        [
            [1, 2, 3]
            [2, 1, 9]
        ]
        """
