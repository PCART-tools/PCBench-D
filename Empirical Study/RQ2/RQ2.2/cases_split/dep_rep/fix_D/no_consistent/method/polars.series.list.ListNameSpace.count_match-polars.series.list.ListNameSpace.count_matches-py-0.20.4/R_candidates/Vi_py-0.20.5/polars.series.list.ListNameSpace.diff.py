    def diff(self, n: int = 1, null_behavior: NullBehavior = "ignore") -> Series:
        """
        Calculate the first discrete difference between shifted items of every sublist.

        Parameters
        ----------
        n
            Number of slots to shift.
        null_behavior : {'ignore', 'drop'}
            How to handle null values.

        Examples
        --------
        >>> s = pl.Series("a", [[1, 2, 3, 4], [10, 2, 1]])
        >>> s.list.diff()
        shape: (2,)
        Series: 'a' [list[i64]]
        [
            [null, 1, … 1]
            [null, -8, -1]
        ]

        >>> s.list.diff(n=2)
        shape: (2,)
        Series: 'a' [list[i64]]
        [
            [null, null, … 2]
            [null, null, -9]
        ]

        >>> s.list.diff(n=2, null_behavior="drop")
        shape: (2,)
        Series: 'a' [list[i64]]
        [
            [2, 2]
            [-9]
        ]
        """
