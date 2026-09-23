    def gather_every(
        self, n: int | IntoExprColumn, offset: int | IntoExprColumn = 0
    ) -> Series:
        """
        Take every n-th value start from offset in sublists.

        Parameters
        ----------
        n
            Gather every n-th element.
        offset
            Starting index.

        Examples
        --------
        >>> s = pl.Series("a", [[1, 2, 3], [], [6, 7, 8, 9]])
        >>> s.list.gather_every(2, offset=1)
        shape: (3,)
        Series: 'a' [list[i64]]
        [
            [2]
            []
            [7, 9]
        ]
        """
