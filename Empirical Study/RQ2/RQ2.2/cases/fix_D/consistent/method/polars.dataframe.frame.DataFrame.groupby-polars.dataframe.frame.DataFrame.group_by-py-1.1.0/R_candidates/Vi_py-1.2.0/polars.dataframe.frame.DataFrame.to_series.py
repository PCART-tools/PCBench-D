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
        return wrap_s(self._df.to_series(index))
