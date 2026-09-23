    def shift(self, n: int | IntoExprColumn = 1) -> Series:
        """
        Shift array values by the given number of indices.

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
        By default, array values are shifted forward by one index.

        >>> s = pl.Series([[1, 2, 3], [4, 5, 6]], dtype=pl.Array(pl.Int64, 3))
        >>> s.arr.shift()
        shape: (2,)
        Series: '' [array[i64, 3]]
        [
            [null, 1, 2]
            [null, 4, 5]
        ]

        Pass a negative value to shift in the opposite direction instead.

        >>> s.arr.shift(-2)
        shape: (2,)
        Series: '' [array[i64, 3]]
        [
            [3, null, null]
            [6, null, null]
        ]
        """
