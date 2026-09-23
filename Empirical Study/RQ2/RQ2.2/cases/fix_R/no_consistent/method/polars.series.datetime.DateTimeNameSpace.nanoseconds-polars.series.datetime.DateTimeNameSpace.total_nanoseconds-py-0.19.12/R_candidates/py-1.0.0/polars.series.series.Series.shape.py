    @property
    def shape(self) -> tuple[int]:
        """
        Shape of this Series.

        Examples
        --------
        >>> s = pl.Series("a", [1, 2, 3])
        >>> s.shape
        (3,)
        """
        return (self._s.len(),)
