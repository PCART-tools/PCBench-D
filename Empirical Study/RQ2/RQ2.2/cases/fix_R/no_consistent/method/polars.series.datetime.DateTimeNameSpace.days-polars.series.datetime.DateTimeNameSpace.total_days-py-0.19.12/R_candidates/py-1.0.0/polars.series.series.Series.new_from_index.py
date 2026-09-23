    def new_from_index(self, index: int, length: int) -> Self:
        """
        Create a new Series filled with values from the given index.

        Examples
        --------
        >>> s = pl.Series("a", [1, 2, 3, 4, 5])
        >>> s.new_from_index(1, 3)
        shape: (3,)
        Series: 'a' [i64]
        [
            2
            2
            2
        ]
        """
        return self._from_pyseries(self._s.new_from_index(index, length))
