    @property
    def name(self) -> str:
        """
        Get the name of this Series.

        Examples
        --------
        >>> s = pl.Series("a", [1, 2, 3])
        >>> s.name
        'a'
        """
        return self._s.name()
