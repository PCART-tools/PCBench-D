    @unstable()
    def uses_lexical_ordering(self) -> bool:
        """
        Return whether or not the series uses lexical ordering.

        .. warning::
            This functionality is considered **unstable**. It may be changed
            at any point without it being considered a breaking change.

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
