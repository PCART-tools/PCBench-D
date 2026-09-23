    def unique(self, *, maintain_order: bool = False) -> Series:
        """
        Get the unique/distinct values in the list.

        Parameters
        ----------
        maintain_order
            Maintain order of data. This requires more work.

        Examples
        --------
        >>> s = pl.Series("a", [[1, 1, 2], [2, 3, 3]])
        >>> s.list.unique()
        shape: (2,)
        Series: 'a' [list[i64]]
        [
            [1, 2]
            [2, 3]
        ]
        """
