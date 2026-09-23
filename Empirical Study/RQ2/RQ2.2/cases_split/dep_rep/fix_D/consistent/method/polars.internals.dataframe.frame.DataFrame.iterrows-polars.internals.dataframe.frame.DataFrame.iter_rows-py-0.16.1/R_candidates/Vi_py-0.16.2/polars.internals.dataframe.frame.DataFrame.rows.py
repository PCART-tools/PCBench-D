    def rows(self, named: bool = False) -> list[tuple[Any, ...]] | list[dict[str, Any]]:
        """
        Returns all data in the DataFrame as a list of rows of python-native values.

        Parameters
        ----------
        named
            Return dictionaries instead of tuples. The dictionaries are a mapping of
            column name to row value. This is more expensive than returning a regular
            tuple, but allows for accessing values by column name.

        Notes
        -----
        If you have ``ns``-precision temporal values you should be aware that python
        natively only supports up to ``us``-precision; if this matters you should export
        to a different format.

        Warnings
        --------
        Row-iteration is not optimal as the underlying data is stored in columnar form;
        where possible, prefer export via one of the dedicated export/output methods.

        Returns
        -------
        A list of tuples (default) or dictionaries of row values.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "a": [1, 3, 5],
        ...         "b": [2, 4, 6],
        ...     }
        ... )
        >>> df.rows()
        [(1, 2), (3, 4), (5, 6)]
        >>> df.rows(named=True)
        [{'a': 1, 'b': 2}, {'a': 3, 'b': 4}, {'a': 5, 'b': 6}]

        See Also
        --------
        iter_rows : Row iterator over frame data (does not materialise all rows).

        """
        if named:
            # Load these into the local namespace for a minor performance boost
            dict_, zip_, columns = dict, zip, self.columns
            return [dict_(zip_(columns, row)) for row in self._df.row_tuples()]
        else:
            return self._df.row_tuples()
