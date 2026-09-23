    def to_list(self) -> list[Any]:
        """
        Convert this Series to a Python list.

        This operation copies data.

        Examples
        --------
        >>> s = pl.Series("a", [1, 2, 3])
        >>> s.to_list()
        [1, 2, 3]
        >>> type(s.to_list())
        <class 'list'>
        """
        return self._s.to_list()
