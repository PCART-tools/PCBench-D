    @deprecate_function("Use `Series.dtype == pl.Boolean` instead.", version="0.19.14")
    def is_boolean(self) -> bool:
        """
        Check if this Series is a Boolean.

        .. deprecated:: 0.19.14
            Use `Series.dtype == pl.Boolean` instead.

        Examples
        --------
        >>> s = pl.Series("a", [True, False, True])
        >>> s.is_boolean()  # doctest: +SKIP
        True

        """
        return self.dtype == Boolean
