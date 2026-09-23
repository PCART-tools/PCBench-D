    def clone(self) -> Self:
        """
        Create a copy of this LazyFrame.

        This is a cheap operation that does not copy data.

        See Also
        --------
        clear : Create an empty copy of the current LazyFrame, with identical
            schema but no data.

        Examples
        --------
        >>> lf = pl.LazyFrame(
        ...     {
        ...         "a": [None, 2, 3, 4],
        ...         "b": [0.5, None, 2.5, 13],
        ...         "c": [True, True, False, None],
        ...     }
        ... )
        >>> lf.clone()  # doctest: +ELLIPSIS
        <LazyFrame [3 cols, {"a": Int64 … "c": Boolean}] at ...>

        """
        return self._from_pyldf(self._ldf.clone())
