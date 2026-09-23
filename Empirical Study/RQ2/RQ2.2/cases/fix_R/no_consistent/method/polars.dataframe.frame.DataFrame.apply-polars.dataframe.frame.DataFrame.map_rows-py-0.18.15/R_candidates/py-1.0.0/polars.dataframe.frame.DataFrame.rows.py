    def rows(
        self, *, named: bool = False
    ) -> list[tuple[Any, ...]] | list[dict[str, Any]]:
        """
        Returns all data in the DataFrame as a list of rows of python-native values.

        By default, each row is returned as a tuple of values given in the same order
        as the frame columns. Setting `named=True` will return rows of dictionaries
        instead.

        Parameters
        ----------
        named
            Return dictionaries instead of tuples. The dictionaries are a mapping of
            column name to row value. This is more expensive than returning a regular
            tuple, but allows for accessing values by column name.

        Notes
        -----
        If you have `ns`-precision temporal values you should be aware that Python
        natively only supports up to `μs`-precision; `ns`-precision values will be
        truncated to microseconds on conversion to Python. If this matters to your
        use-case you should export to a different format (such as Arrow or NumPy).

        Warnings
        --------
        Row-iteration is not optimal as the underlying data is stored in columnar form;
        where possible, prefer export via one of the dedicated export/output methods.
        You should also consider using `iter_rows` instead, to avoid materialising all
        the data at once; there is little performance difference between the two, but
        peak memory can be reduced if processing rows in batches.

        Returns
        -------
        list of row value tuples (default), or list of dictionaries (if `named=True`).

        See Also
        --------
        iter_rows : Row iterator over frame data (does not materialise all rows).
        rows_by_key : Materialises frame data as a key-indexed dictionary.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "x": ["a", "b", "b", "a"],
        ...         "y": [1, 2, 3, 4],
        ...         "z": [0, 3, 6, 9],
        ...     }
        ... )
        >>> df.rows()
        [('a', 1, 0), ('b', 2, 3), ('b', 3, 6), ('a', 4, 9)]
        >>> df.rows(named=True)
        [{'x': 'a', 'y': 1, 'z': 0},
         {'x': 'b', 'y': 2, 'z': 3},
         {'x': 'b', 'y': 3, 'z': 6},
         {'x': 'a', 'y': 4, 'z': 9}]
        """
        if named:
            # Load these into the local namespace for a minor performance boost
            dict_, zip_, columns = dict, zip, self.columns
            return [dict_(zip_(columns, row)) for row in self._df.row_tuples()]
        else:
            return self._df.row_tuples()
