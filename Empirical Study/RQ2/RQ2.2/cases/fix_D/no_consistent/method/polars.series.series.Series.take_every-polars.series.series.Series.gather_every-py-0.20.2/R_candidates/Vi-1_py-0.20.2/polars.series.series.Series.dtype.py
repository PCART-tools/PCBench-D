    @property
    def dtype(self) -> DataType:
        """
        Get the data type of this Series.

        Examples
        --------
        >>> s = pl.Series("a", [1, 2, 3])
        >>> s.dtype
        Int64

        """
        return self._s.dtype()
