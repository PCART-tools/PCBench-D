    def count(self) -> int:
        """
        Return the number of non-null elements in the column.

        See Also
        --------
        len

        Examples
        --------
        >>> s = pl.Series("a", [1, 2, None])
        >>> s.count()
        2
        """
        return self.len() - self.null_count()
