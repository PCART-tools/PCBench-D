    def last(self) -> Series:
        """
        Get the last value of the sublists.

        Examples
        --------
        >>> s = pl.Series("a", [[3, 2, 1], [], [1, 2]])
        >>> s.list.last()
        shape: (3,)
        Series: 'a' [i64]
        [
            1
            null
            2
        ]
        """
