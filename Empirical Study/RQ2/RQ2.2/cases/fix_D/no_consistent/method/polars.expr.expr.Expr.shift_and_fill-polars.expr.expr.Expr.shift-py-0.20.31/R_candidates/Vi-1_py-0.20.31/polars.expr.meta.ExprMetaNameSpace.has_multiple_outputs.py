    def has_multiple_outputs(self) -> bool:
        """
        Indicate if this expression expands into multiple expressions.

        Examples
        --------
        >>> e = pl.col(["a", "b"]).name.suffix("_foo")
        >>> e.meta.has_multiple_outputs()
        True
        """
        return self._pyexpr.meta_has_multiple_outputs()
