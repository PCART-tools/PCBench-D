    def iter_rows(
        self, *, named: bool = False, buffer_size: int = 512
    ) -> Iterator[tuple[Any, ...]] | Iterator[dict[str, Any]]:
        """
        Returns an iterator over the DataFrame of rows of python-native values.

        Parameters
        ----------
        named
            Return dictionaries instead of tuples. The dictionaries are a mapping of
            column name to row value. This is more expensive than returning a regular
            tuple, but allows for accessing values by column name.
        buffer_size
            Determines the number of rows that are buffered internally while iterating
            over the data; you should only modify this in very specific cases where the
            default value is determined not to be a good fit to your access pattern, as
            the speedup from using the buffer is significant (~2-4x). Setting this
            value to zero disables row buffering (not recommended).

        Notes
        -----
        If you have `ns`-precision temporal values you should be aware that Python
        natively only supports up to `μs`-precision; `ns`-precision values will be
        truncated to microseconds on conversion to Python. If this matters to your
        use-case you should export to a different format (such as Arrow or NumPy).

        Warnings
        --------
        Row iteration is not optimal as the underlying data is stored in columnar form;
        where possible, prefer export via one of the dedicated export/output methods
        that deals with columnar data.

        Returns
        -------
        iterator of tuples (default) or dictionaries (if named) of python row values

        See Also
        --------
        rows : Materialises all frame data as a list of rows (potentially expensive).
        rows_by_key : Materialises frame data as a key-indexed dictionary.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "a": [1, 3, 5],
        ...         "b": [2, 4, 6],
        ...     }
        ... )
        >>> [row[0] for row in df.iter_rows()]
        [1, 3, 5]
        >>> [row["b"] for row in df.iter_rows(named=True)]
        [2, 4, 6]

        """
        # load into the local namespace for a (minor) performance boost in the hot loops
        columns, get_row, dict_, zip_ = self.columns, self.row, dict, zip
        has_object = Object in self.dtypes

        # note: buffering rows results in a 2-4x speedup over individual calls
        # to ".row(i)", so it should only be disabled in extremely specific cases.
        if buffer_size and not has_object:
            for offset in range(0, self.height, buffer_size):
                zerocopy_slice = self.slice(offset, buffer_size)
                if named:
                    for row in zerocopy_slice.rows(named=False):
                        yield dict_(zip_(columns, row))
                else:
                    yield from zerocopy_slice.rows(named=False)
        elif named:
            for i in range(self.height):
                yield dict_(zip_(columns, get_row(i)))
        else:
            for i in range(self.height):
                yield get_row(i)
