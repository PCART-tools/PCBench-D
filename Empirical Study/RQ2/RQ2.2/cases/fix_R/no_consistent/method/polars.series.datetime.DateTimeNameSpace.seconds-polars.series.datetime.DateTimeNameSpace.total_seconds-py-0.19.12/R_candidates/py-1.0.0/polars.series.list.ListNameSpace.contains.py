    def contains(
        self, item: float | str | bool | int | date | datetime | time | IntoExprColumn
    ) -> Series:
        """
        Check if sublists contain the given item.

        Parameters
        ----------
        item
            Item that will be checked for membership

        Returns
        -------
        Series
            Series of data type :class:`Boolean`.

        Examples
        --------
        >>> s = pl.Series("a", [[3, 2, 1], [], [1, 2]])
        >>> s.list.contains(1)
        shape: (3,)
        Series: 'a' [bool]
        [
            true
            false
            true
        ]
        """
