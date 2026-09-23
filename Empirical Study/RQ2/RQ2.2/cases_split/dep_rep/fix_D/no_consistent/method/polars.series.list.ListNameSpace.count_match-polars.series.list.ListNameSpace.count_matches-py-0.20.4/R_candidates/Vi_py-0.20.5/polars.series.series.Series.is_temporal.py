    @deprecate_function("Use `Series.dtype.is_temporal()` instead.", version="0.19.13")
    def is_temporal(self, excluding: OneOrMoreDataTypes | None = None) -> bool:
        """
        Check if this Series datatype is temporal.

        .. deprecated:: 0.19.13
            Use `Series.dtype.is_temporal()` instead.

        Parameters
        ----------
        excluding
            Optionally exclude one or more temporal dtypes from matching.

        Examples
        --------
        >>> from datetime import date
        >>> s = pl.Series([date(2021, 1, 1), date(2021, 1, 2), date(2021, 1, 3)])
        >>> s.is_temporal()  # doctest: +SKIP
        True
        >>> s.is_temporal(excluding=[pl.Date])  # doctest: +SKIP
        False
        """
        if excluding is not None:
            if not isinstance(excluding, Iterable):
                excluding = [excluding]
            if self.dtype in excluding:
                return False

        return self.dtype.is_temporal()
