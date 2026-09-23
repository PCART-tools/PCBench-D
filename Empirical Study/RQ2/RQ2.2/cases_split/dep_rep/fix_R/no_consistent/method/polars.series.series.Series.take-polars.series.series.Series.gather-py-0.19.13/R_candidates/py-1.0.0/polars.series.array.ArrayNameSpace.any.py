    def any(self) -> Series:
        """
        Evaluate whether any boolean value is true for every subarray.

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
        >>> s.arr.any()
        shape: (5,)
        Series: '' [bool]
        [
            true
            true
            false
            false
            null
        ]
        """
