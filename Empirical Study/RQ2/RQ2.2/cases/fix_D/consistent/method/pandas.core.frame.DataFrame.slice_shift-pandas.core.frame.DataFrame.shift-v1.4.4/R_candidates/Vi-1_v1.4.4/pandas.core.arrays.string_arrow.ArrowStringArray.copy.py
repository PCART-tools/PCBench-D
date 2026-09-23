    def copy(self) -> ArrowStringArray:
        """
        Return a shallow copy of the array.

        Underlying ChunkedArray is immutable, so a deep copy is unnecessary.

        Returns
        -------
        ArrowStringArray
        """
        return type(self)(self._data)
