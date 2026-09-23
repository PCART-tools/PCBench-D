    def unique(self, *, maintain_order: bool = False) -> Series:
        """
        Get the unique/distinct values in the array.

        Parameters
        ----------
        maintain_order
            Maintain order of data. This requires more work.

        Returns
        -------
        Series
            Series of data type :class:`List`.

        Examples
        --------
        >>> s = pl.Series([[1, 1, 2], [3, 4, 5]], dtype=pl.Array(pl.Int64, 3))
        >>> s.arr.unique()
        shape: (2,)
        Series: '' [list[i64]]
        [
            [1, 2]
            [3, 4, 5]
        ]
        """
