    @property
    def width(self) -> int:
        """
        Get the number of columns.

        Returns
        -------
        int

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "foo": [1, 2, 3],
        ...         "bar": [4, 5, 6],
        ...     }
        ... )
        >>> df.width
        2
        """
        return self._df.width()
