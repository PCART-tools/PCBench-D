    def has_multiple_outputs(self) -> bool:
        """
        Whether this expression expands into multiple expressions.

        Examples
        --------
        >>> e = pl.col(["a", "b"]).alias("bar")
        >>> e.meta.has_multiple_outputs()
        True

        """
        return self._pyexpr.meta_has_multiple_outputs()
