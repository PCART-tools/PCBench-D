    @deprecate_function("Use `Series.dtype.is_numeric()` instead.", version="0.19.13")
    def is_numeric(self) -> bool:
        """
        Check if this Series datatype is numeric.

        .. deprecated:: 0.19.13
            Use `Series.dtype.is_numeric()` instead.

        Examples
        --------
        >>> s = pl.Series("a", [1, 2, 3])
        >>> s.is_numeric()  # doctest: +SKIP
        True
        """
        return self.dtype.is_numeric()
