    def is_empty(self) -> bool:
        """
        Returns `True` if the DataFrame contains no rows.

        Examples
        --------
        >>> df = pl.DataFrame({"foo": [1, 2, 3], "bar": [4, 5, 6]})
        >>> df.is_empty()
        False
        >>> df.filter(pl.col("foo") > 99).is_empty()
        True
        """
        return self._df.is_empty()
