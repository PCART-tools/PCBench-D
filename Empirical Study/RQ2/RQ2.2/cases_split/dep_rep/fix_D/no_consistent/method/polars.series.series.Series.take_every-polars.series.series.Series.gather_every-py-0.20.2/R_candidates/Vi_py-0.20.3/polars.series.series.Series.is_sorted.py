    def is_sorted(self, *, descending: bool = False) -> bool:
        """
        Check if the Series is sorted.

        Parameters
        ----------
        descending
            Check if the Series is sorted in descending order

        Examples
        --------
        >>> s = pl.Series([1, 3, 2])
        >>> s.is_sorted()
        False

        >>> s = pl.Series([3, 2, 1])
        >>> s.is_sorted(descending=True)
        True

        """
        return self._s.is_sorted(descending)
