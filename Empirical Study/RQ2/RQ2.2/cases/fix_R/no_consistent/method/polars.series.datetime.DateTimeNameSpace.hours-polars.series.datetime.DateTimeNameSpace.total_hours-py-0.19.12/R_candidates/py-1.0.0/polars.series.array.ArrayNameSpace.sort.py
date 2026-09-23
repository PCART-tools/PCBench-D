    def sort(
        self,
        *,
        descending: bool = False,
        nulls_last: bool = False,
        multithreaded: bool = True,
    ) -> Series:
        """
        Sort the arrays in this column.

        Parameters
        ----------
        descending
            Sort in descending order.
        nulls_last
            Place null values last.
        multithreaded
            Sort using multiple threads.

        Examples
        --------
        >>> s = pl.Series("a", [[3, 2, 1], [9, 1, 2]], dtype=pl.Array(pl.Int64, 3))
        >>> s.arr.sort()
        shape: (2,)
        Series: 'a' [array[i64, 3]]
        [
            [1, 2, 3]
            [1, 2, 9]
        ]
        >>> s.arr.sort(descending=True)
        shape: (2,)
        Series: 'a' [array[i64, 3]]
        [
            [3, 2, 1]
            [9, 2, 1]
        ]

        """
