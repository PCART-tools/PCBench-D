    def get(self, index: int | IntoExprColumn, *, null_on_oob: bool = False) -> Series:
        """
        Get the value by index in the sub-arrays.

        So index `0` would return the first item of every sublist
        and index `-1` would return the last item of every sublist
        if an index is out of bounds, it will return a `None`.

        Parameters
        ----------
        index
            Index to return per sublist
        null_on_oob
            Behavior if an index is out of bounds:
            True -> set as null
            False -> raise an error

        Returns
        -------
        Series
            Series of innter data type.

        Examples
        --------
        >>> s = pl.Series(
        ...     "a", [[1, 2, 3], [4, 5, 6], [7, 8, 9]], dtype=pl.Array(pl.Int32, 3)
        ... )
        >>> s.arr.get(pl.Series([1, -2, 0]), null_on_oob=True)
        shape: (3,)
        Series: 'a' [i32]
        [
            2
            5
            7
        ]

        """
