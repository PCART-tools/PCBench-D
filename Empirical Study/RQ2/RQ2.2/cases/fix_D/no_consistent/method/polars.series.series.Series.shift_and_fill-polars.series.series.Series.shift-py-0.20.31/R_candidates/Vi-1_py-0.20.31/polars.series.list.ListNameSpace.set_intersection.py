    def set_intersection(self, other: Series) -> Series:
        """
        Compute the SET INTERSECTION between the elements in this list and the elements of `other`.

        Parameters
        ----------
        other
            Right hand side of the set operation.

        Examples
        --------
        >>> a = pl.Series([[1, 2, 3], [], [None, 3], [5, 6, 7]])
        >>> b = pl.Series([[2, 3, 4], [3], [3, 4, None], [6, 8]])
        >>> a.list.set_intersection(b)
        shape: (4,)
        Series: '' [list[i64]]
        [
                [2, 3]
                []
                [null, 3]
                [6]
        ]
        """  # noqa: W505
