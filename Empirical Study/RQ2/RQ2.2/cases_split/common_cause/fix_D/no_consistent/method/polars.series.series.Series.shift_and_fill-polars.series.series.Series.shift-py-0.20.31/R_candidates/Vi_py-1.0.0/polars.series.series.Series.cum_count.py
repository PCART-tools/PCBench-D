    def cum_count(self, *, reverse: bool = False) -> Self:
        """
        Return the cumulative count of the non-null values in the column.

        Parameters
        ----------
        reverse
            Reverse the operation.

        Examples
        --------
        >>> s = pl.Series(["x", "k", None, "d"])
        >>> s.cum_count()
        shape: (4,)
        Series: '' [u32]
        [
                1
                2
                2
                3
        ]
        """
