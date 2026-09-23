    @property
    def width(self) -> int:
        """
        Get the width of the LazyFrame.

        Examples
        --------
        >>> lf = pl.LazyFrame(
        ...     {
        ...         "foo": [1, 2, 3],
        ...         "bar": [4, 5, 6],
        ...     }
        ... )
        >>> lf.width
        2

        """
        return self._ldf.width()
