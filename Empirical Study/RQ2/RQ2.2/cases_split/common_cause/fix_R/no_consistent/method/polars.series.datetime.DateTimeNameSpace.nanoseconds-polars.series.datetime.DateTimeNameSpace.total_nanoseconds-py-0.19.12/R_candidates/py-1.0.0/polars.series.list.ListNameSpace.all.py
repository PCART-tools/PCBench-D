    def all(self) -> Series:
        """
        Evaluate whether all boolean values in a list are true.

        Returns
        -------
        Series
            Series of data type :class:`Boolean`.

        Examples
        --------
        >>> s = pl.Series(
        ...     [[True, True], [False, True], [False, False], [None], [], None],
        ...     dtype=pl.List(pl.Boolean),
        ... )
        >>> s.list.all()
        shape: (6,)
        Series: '' [bool]
        [
            true
            false
            false
            true
            true
            null
        ]
        """
