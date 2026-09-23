    def any(self) -> Series:
        """
        Evaluate whether any boolean value in a list is true.

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
        >>> s.list.any()
        shape: (6,)
        Series: '' [bool]
        [
            true
            true
            false
            false
            false
            null
        ]

        """
