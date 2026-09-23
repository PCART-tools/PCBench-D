    def get_column(self, name: str) -> Series:
        """
        Get a single column by name.

        Parameters
        ----------
        name : str
            Name of the column to retrieve.

        Returns
        -------
        Series

        See Also
        --------
        to_series

        Examples
        --------
        >>> df = pl.DataFrame({"foo": [1, 2, 3], "bar": [4, 5, 6]})
        >>> df.get_column("foo")
        shape: (3,)
        Series: 'foo' [i64]
        [
                1
                2
                3
        ]

        """
        return wrap_s(self._df.get_column(name))
