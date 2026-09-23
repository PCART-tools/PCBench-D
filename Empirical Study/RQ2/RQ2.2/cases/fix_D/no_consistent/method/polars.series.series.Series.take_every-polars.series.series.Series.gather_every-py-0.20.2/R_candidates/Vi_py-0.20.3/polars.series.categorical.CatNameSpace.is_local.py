    def is_local(self) -> bool:
        """
        Return whether or not the column is a local categorical.

        Examples
        --------
        Categoricals constructed without a string cache are considered local.

        >>> s = pl.Series(["a", "b", "a"], dtype=pl.Categorical)
        >>> s.cat.is_local()
        True

        Categoricals constructed with a string cache are considered global.

        >>> with pl.StringCache():
        ...     s = pl.Series(["a", "b", "a"], dtype=pl.Categorical)
        >>> s.cat.is_local()
        False

        """
        return self._s.cat_is_local()
