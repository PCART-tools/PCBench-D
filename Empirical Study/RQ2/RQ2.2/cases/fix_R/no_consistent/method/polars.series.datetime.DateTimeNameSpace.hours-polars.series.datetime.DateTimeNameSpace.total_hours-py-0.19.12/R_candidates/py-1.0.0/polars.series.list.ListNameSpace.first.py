    def first(self) -> Series:
        """
        Get the first value of the sublists.

        Examples
        --------
        >>> s = pl.Series("a", [[3, 2, 1], [], [1, 2]])
        >>> s.list.first()
        shape: (3,)
        Series: 'a' [i64]
        [
            3
            null
            1
        ]
        """
