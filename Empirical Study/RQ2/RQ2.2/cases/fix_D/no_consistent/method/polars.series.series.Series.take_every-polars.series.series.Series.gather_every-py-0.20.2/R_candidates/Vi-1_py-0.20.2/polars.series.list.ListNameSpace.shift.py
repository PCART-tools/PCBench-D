    @deprecate_renamed_parameter("periods", "n", version="0.19.11")
    def shift(self, n: int | IntoExprColumn = 1) -> Series:
        """
        Shift list values by the given number of indices.

        Parameters
        ----------
        n
            Number of indices to shift forward. If a negative value is passed, values
            are shifted in the opposite direction instead.

        Notes
        -----
        This method is similar to the `LAG` operation in SQL when the value for `n`
        is positive. With a negative value for `n`, it is similar to `LEAD`.

        Examples
        --------
        By default, list values are shifted forward by one index.

        >>> s = pl.Series([[1, 2, 3], [4, 5]])
        >>> s.list.shift()
        shape: (2,)
        Series: '' [list[i64]]
        [
                [null, 1, 2]
                [null, 4]
        ]

        Pass a negative value to shift in the opposite direction instead.

        >>> s.list.shift(-2)
        shape: (2,)
        Series: '' [list[i64]]
        [
                [3, null, null]
                [null, null]
        ]

        """
