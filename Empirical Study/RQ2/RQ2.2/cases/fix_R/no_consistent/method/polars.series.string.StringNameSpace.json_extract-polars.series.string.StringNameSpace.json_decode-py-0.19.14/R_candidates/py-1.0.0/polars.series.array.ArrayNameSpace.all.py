    def all(self) -> Series:
        """
        Evaluate whether all boolean values are true for every subarray.

        Returns
        -------
        Series
            Series of data type :class:`Boolean`.

        Examples
        --------
        >>> s = pl.Series(
        ...     [[True, True], [False, True], [False, False], [None, None], None],
        ...     dtype=pl.Array(pl.Boolean, 2),
        ... )
        >>> s.arr.all()
        shape: (5,)
        Series: '' [bool]
        [
            true
            false
            false
            true
            null
        ]
        """
