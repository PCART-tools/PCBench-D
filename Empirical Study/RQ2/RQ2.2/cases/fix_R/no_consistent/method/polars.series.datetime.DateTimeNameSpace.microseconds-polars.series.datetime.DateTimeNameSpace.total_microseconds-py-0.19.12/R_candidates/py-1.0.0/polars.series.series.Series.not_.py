    def not_(self) -> Series:
        """
        Negate a boolean Series.

        Returns
        -------
        Series
            Series of data type :class:`Boolean`.

        Examples
        --------
        >>> s = pl.Series("a", [True, False, False])
        >>> s.not_()
        shape: (3,)
        Series: 'a' [bool]
        [
            false
            true
            true
        ]
        """
        return self._from_pyseries(self._s.not_())
