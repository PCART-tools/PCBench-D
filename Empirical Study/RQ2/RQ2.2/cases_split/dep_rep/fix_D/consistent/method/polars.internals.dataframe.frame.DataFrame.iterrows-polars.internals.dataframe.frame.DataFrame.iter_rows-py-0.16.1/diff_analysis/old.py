    def iter_rows(
        self, named: bool = False, buffer_size: int = 500
    ) -> Iterator[tuple[Any, ...]] | Iterator[dict[str, Any]]:
        """
        Returns an iterator over the rows of the DataFrame.

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
            value to zero disables row buffering.

        Returns
        -------
        An iterator of tuples (default) or dictionaries of row values.

        Warnings
        --------
        Row iteration is not optimal as the underlying data is stored in columnar form;
        where possible, prefer export via one of the dedicated export/output methods.

        Notes
        -----
        If you are planning to materialise all frame data at once you should prefer
        calling ``rows()``, which will be faster.

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

        See Also
        --------
        rows : Materialises all frame data as a list of rows.

        """
        # load into the local namespace for a modest performance boost in the hot loops
        columns, get_row, dict_, zip_ = self.columns, self.row, dict, zip

        # note: buffering rows results in a 2-4x speedup over individual calls
        # to ".row(i)", so it should only be disabled in extremely specific cases.
        if buffer_size:
            for offset in range(0, self.height, buffer_size):
                zerocopy_slice = self.slice(offset, buffer_size)
                if named and _PYARROW_AVAILABLE:
                    yield from zerocopy_slice.to_arrow().to_batches()[0].to_pylist()
                else:
                    rows_chunk = zerocopy_slice.rows(named=False)
                    if named:
                        for row in rows_chunk:
                            yield dict_(zip_(columns, row))
                    else:
                        yield from rows_chunk
        elif named:
            for i in range(self.height):
                yield dict_(zip_(columns, get_row(i)))
        else:
            for i in range(self.height):
                yield get_row(i)
