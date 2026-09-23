    @deprecate_function("Use `Series.dtype.is_float()` instead.", version="0.19.13")
    def is_float(self) -> bool:
        """
        Check if this Series has floating point numbers.

        .. deprecated:: 0.19.13
            Use `Series.dtype.is_float()` instead.

        Examples
        --------
        >>> s = pl.Series("a", [1.0, 2.0, 3.0])
        >>> s.is_float()  # doctest: +SKIP
        True

        """
        return self.dtype.is_float()
