    def get_column(
        self, name: str, *, default: Any | NoDefault = no_default
    ) -> Series | Any:
        """
        Get a single column by name.

        Parameters
        ----------
        name
            String name of the column to retrieve.
        default
            Value to return if the column does not exist; if not explicitly set and
            the column is not present a `ColumnNotFoundError` exception is raised.

        Returns
        -------
        Series (or arbitrary default value, if specified).

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

        Missing column handling; can optionally provide an arbitrary default value
        to the method (otherwise a `ColumnNotFoundError` exception is raised).

        >>> df.get_column("baz", default=pl.Series("baz", ["?", "?", "?"]))
        shape: (3,)
        Series: 'baz' [str]
        [
            "?"
            "?"
            "?"
        ]
        >>> res = df.get_column("baz", default=None)
        >>> res is None
        True
        """
        try:
            return wrap_s(self._df.get_column(name))
        except ColumnNotFoundError:
            if default is no_default:
                raise
            return default
