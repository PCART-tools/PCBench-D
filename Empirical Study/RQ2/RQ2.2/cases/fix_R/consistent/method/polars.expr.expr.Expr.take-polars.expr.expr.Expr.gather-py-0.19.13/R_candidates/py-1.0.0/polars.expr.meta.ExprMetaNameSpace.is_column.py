    def is_column(self) -> bool:
        r"""
        Indicate if this expression is a basic (non-regex) unaliased column.

        Examples
        --------
        >>> e = pl.col("foo")
        >>> e.meta.is_column()
        True
        >>> e = pl.col("foo") * pl.col("bar")
        >>> e.meta.is_column()
        False
        >>> e = pl.col(r"^col.*\d+$")
        >>> e.meta.is_column()
        False
        """
        return self._pyexpr.meta_is_column()
