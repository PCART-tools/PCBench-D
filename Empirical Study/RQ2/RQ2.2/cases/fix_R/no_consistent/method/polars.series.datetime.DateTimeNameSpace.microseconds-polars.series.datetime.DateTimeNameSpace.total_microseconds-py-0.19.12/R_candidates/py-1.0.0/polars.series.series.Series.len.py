    def len(self) -> int:
        """
        Return the number of elements in the Series.

        Null values count towards the total.

        See Also
        --------
        count

        Examples
        --------
        >>> s = pl.Series("a", [1, 2, None])
        >>> s.len()
        3
        """
        return self._s.len()
