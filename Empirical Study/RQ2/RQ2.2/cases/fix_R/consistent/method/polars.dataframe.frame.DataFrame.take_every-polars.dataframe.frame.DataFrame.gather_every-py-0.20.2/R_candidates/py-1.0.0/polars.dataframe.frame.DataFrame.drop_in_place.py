    def drop_in_place(self, name: str) -> Series:
        """
        Drop a single column in-place and return the dropped column.

        Parameters
        ----------
        name
            Name of the column to drop.

        Returns
        -------
        Series
            The dropped column.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "foo": [1, 2, 3],
        ...         "bar": [6, 7, 8],
        ...         "ham": ["a", "b", "c"],
        ...     }
        ... )
        >>> df.drop_in_place("ham")
        shape: (3,)
        Series: 'ham' [str]
        [
            "a"
            "b"
            "c"
        ]
        """
        return wrap_s(self._df.drop_in_place(name))
