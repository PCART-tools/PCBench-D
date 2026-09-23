    @property
    def columns(self) -> list[str]:
        """
        Get column names.

        Examples
        --------
        >>> lf = pl.LazyFrame(
        ...     {
        ...         "foo": [1, 2, 3],
        ...         "bar": [6, 7, 8],
        ...         "ham": ["a", "b", "c"],
        ...     }
        ... ).select("foo", "bar")
        >>> lf.columns
        ['foo', 'bar']

        """
        return self._ldf.columns()
