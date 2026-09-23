    def set_sorted(self, *, descending: bool = False) -> Self:
        """
        Flags the Series as 'sorted'.

        Enables downstream code to user fast paths for sorted arrays.

        Parameters
        ----------
        descending
            If the `Series` order is descending.

        Warnings
        --------
        This can lead to incorrect results if this `Series` is not sorted!!
        Use with care!

        Examples
        --------
        >>> s = pl.Series("a", [1, 2, 3])
        >>> s.set_sorted().max()
        3

        """
        return self._from_pyseries(self._s.set_sorted_flag(descending))
