    def to_series(self, index: int = 0) -> Series:
        """
        Select column as Series at index location.

        Parameters
        ----------
        index
            Location of selection.

        See Also
        --------
        get_column

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "foo": [1, 2, 3],
        ...         "bar": [6, 7, 8],
        ...         "ham": ["a", "b", "c"],
        ...     }
        ... )
        >>> df.to_series(1)
        shape: (3,)
        Series: 'bar' [i64]
        [
                6
                7
                8
        ]

        """
        if not isinstance(index, int):
            raise TypeError(
                f"index value {index!r} should be an int, but is {type(index).__name__!r}"
            )

        if index < 0:
            index = len(self.columns) + index
        return wrap_s(self._df.select_at_idx(index))
