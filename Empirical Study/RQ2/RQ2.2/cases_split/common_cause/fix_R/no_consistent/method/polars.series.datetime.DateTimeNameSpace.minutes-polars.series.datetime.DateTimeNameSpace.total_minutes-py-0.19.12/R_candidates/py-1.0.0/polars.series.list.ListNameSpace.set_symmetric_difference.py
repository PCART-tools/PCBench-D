    def set_symmetric_difference(self, other: Series) -> Series:
        """
        Compute the SET SYMMETRIC DIFFERENCE between the elements in this list and the elements of `other`.

        Parameters
        ----------
        other
            Right hand side of the set operation.

        Examples
        --------
        >>> a = pl.Series([[1, 2, 3], [], [None, 3], [5, 6, 7]])
        >>> b = pl.Series([[2, 3, 4], [3], [3, 4, None], [6, 8]])
        >>> a.list.set_symmetric_difference(b)
        shape: (4,)
        Series: '' [list[i64]]
        [
            [1, 4]
            [3]
            [4]
            [5, 7, 8]
        ]
        """  # noqa: W505
