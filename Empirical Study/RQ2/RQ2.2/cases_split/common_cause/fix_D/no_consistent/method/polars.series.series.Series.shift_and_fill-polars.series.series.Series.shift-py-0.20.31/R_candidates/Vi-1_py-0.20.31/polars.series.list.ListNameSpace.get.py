    def get(
        self,
        index: int | Series | list[int],
        *,
        null_on_oob: bool = True,
    ) -> Series:
        """
        Get the value by index in the sublists.

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

        Examples
        --------
        >>> s = pl.Series("a", [[3, 2, 1], [], [1, 2]])
        >>> s.list.get(0, null_on_oob=True)
        shape: (3,)
        Series: 'a' [i64]
        [
            3
            null
            1
        ]
        """
