    def null_count(self) -> int:
        """
        Count the null values in this Series.

        Examples
        --------
        >>> s = pl.Series([1, None, None])
        >>> s.null_count()
        2
        """
        return self._s.null_count()
