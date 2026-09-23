    def is_sorted(self, *, descending: bool = False, nulls_last: bool = False) -> bool:
        """
        Check if the Series is sorted.

        Parameters
        ----------
        descending
            Check if the Series is sorted in descending order
        nulls_last
            Set nulls at the end of the Series in sorted check.

        Examples
        --------
        >>> s = pl.Series([1, 3, 2])
        >>> s.is_sorted()
        False

        >>> s = pl.Series([3, 2, 1])
        >>> s.is_sorted(descending=True)
        True
        """
        return self._s.is_sorted(descending, nulls_last)
