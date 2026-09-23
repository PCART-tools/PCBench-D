    def has_nulls(self) -> bool:
        """
        Check whether the Series contains one or more null values.

        Examples
        --------
        >>> s = pl.Series([1, 2, None])
        >>> s.has_nulls()
        True
        >>> s[:2].has_nulls()
        False
        """
        return self.null_count() > 0
