    def uses_lexical_ordering(self) -> bool:
        """
        Return whether or not the series uses lexical ordering.

        This can be set using :func:`set_ordering`.

        Warnings
        --------
        This API is experimental and may change without it being considered a breaking
        change.

        See Also
        --------
        set_ordering

        Examples
        --------
        >>> s = pl.Series(["b", "a", "b"]).cast(pl.Categorical)
        >>> s.cat.uses_lexical_ordering()
        False
        >>> s = s.cast(pl.Categorical("lexical"))
        >>> s.cat.uses_lexical_ordering()
        True
        """
        return self._s.cat_uses_lexical_ordering()
