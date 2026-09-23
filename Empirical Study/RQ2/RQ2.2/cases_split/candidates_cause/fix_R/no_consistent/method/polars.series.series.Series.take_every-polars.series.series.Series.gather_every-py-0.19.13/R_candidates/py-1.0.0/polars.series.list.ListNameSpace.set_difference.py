    def set_difference(self, other: Series) -> Series:
        """
        Compute the SET DIFFERENCE between the elements in this list and the elements of `other`.

        Parameters
        ----------
        other
            Right hand side of the set operation.

        See Also
        --------
        polars.Series.list.diff: Calculates the n-th discrete difference of every sublist.

        Examples
        --------
        >>> a = pl.Series([[1, 2, 3], [], [None, 3], [5, 6, 7]])
        >>> b = pl.Series([[2, 3, 4], [3], [3, 4, None], [6, 8]])
        >>> a.list.set_difference(b)
        shape: (4,)
        Series: '' [list[i64]]
        [
                [1]
                []
                []
                [5, 7]
        ]
        """  # noqa: W505
