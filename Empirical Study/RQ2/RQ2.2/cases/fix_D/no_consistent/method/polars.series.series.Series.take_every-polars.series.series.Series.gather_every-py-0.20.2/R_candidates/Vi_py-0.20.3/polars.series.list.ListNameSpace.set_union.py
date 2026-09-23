    def set_union(self, other: Series) -> Series:
        """
        Compute the SET UNION between the elements in this list and the elements of `other`.

        Parameters
        ----------
        other
            Right hand side of the set operation.

        Examples
        --------
        >>> a = pl.Series([[1, 2, 3], [], [None, 3], [5, 6, 7]])
        >>> b = pl.Series([[2, 3, 4], [3], [3, 4, None], [6, 8]])
        >>> a.list.set_union(b)  # doctest: +IGNORE_RESULT
        shape: (4,)
        Series: '' [list[i64]]
        [
                [1, 2, 3, 4]
                [3]
                [null, 3, 4]
                [5, 6, 7, 8]
        ]

        """  # noqa: W505
