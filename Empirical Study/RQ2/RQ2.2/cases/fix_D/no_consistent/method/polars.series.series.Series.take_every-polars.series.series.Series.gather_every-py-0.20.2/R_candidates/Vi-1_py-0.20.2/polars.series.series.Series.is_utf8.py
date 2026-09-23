    @deprecate_function("Use `Series.dtype == pl.Utf8` instead.", version="0.19.14")
    def is_utf8(self) -> bool:
        """
        Check if this Series datatype is a Utf8.

        .. deprecated:: 0.19.14
            Use `Series.dtype == pl.Utf8` instead.

        Examples
        --------
        >>> s = pl.Series("x", ["a", "b", "c"])
        >>> s.is_utf8()  # doctest: +SKIP
        True

        """
        return self.dtype == Utf8
