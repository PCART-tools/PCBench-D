    def row(
        self,
        index: int | None = None,
        *,
        by_predicate: pli.Expr | None = None,
        named: bool = False,
    ) -> tuple[Any, ...] | dict[str, Any]:
        """
        Get the values of a single row, either by index or by predicate.

        Parameters
        ----------
        index
            Row index.
        by_predicate
            Select the row according to a given expression/predicate.
        named
            Return a dictionary instead of a tuple. The dictionary is a mapping of
            column name to row value. This is more expensive than returning a regular
            tuple, but allows for accessing values by column name.

        Returns
        -------
        Tuple (default) or dictionary of row values.

        Notes
        -----
        The ``index`` and ``by_predicate`` params are mutually exclusive. Additionally,
        to ensure clarity, the `by_predicate` parameter must be supplied by keyword.

        When using ``by_predicate`` it is an error condition if anything other than
        one row is returned; more than one row raises ``TooManyRowsReturned``, and
        zero rows will raise ``NoRowsReturned`` (both inherit from ``RowsException``).

        Warning
        -------
        You should NEVER use this method to iterate over a DataFrame; if you absolutely
        require row-iteration you should strongly prefer ``iter_rows()`` instead.

        Examples
        --------
        Specify an index to return the row at the given index as a tuple.

        >>> df = pl.DataFrame(
        ...     {
        ...         "foo": [1, 2, 3],
        ...         "bar": [6, 7, 8],
        ...         "ham": ["a", "b", "c"],
        ...     }
        ... )
        >>> df.row(2)
        (3, 8, 'c')

        Specify ``named=True`` to get a dictionary instead with a mapping of column
        names to row values.

        >>> df.row(2, named=True)
        {'foo': 3, 'bar': 8, 'ham': 'c'}

        Use ``by_predicate`` to return the row that matches the given predicate.

        >>> df.row(by_predicate=(pl.col("ham") == "b"))
        (2, 7, 'b')

        See Also
        --------
        iter_rows : Row iterator over frame data (does not materialise all rows).
        rows : Materialises all frame data as a list of rows.

        """
        if index is not None and by_predicate is not None:
            raise ValueError(
                "Cannot set both 'index' and 'by_predicate'; mutually exclusive"
            )
        elif isinstance(index, pli.Expr):
            raise TypeError("Expressions should be passed to the 'by_predicate' param")

        if index is not None:
            row = self._df.row_tuple(index)
            if named:
                return dict(zip(self.columns, row))
            else:
                return row

        elif by_predicate is not None:
            if not isinstance(by_predicate, pli.Expr):
                raise TypeError(
                    f"Expected 'by_predicate to be an expression; "
                    f"found {type(by_predicate)}"
                )
            rows = self.filter(by_predicate).rows()
            n_rows = len(rows)
            if n_rows > 1:
                raise TooManyRowsReturned(
                    f"Predicate <{by_predicate!s}> returned {n_rows} rows"
                )
            elif n_rows == 0:
                raise NoRowsReturned(f"Predicate <{by_predicate!s}> returned no rows")

            row = rows[0]
            if named:
                return dict(zip(self.columns, row))
            else:
                return row
        else:
            raise ValueError("One of 'index' or 'by_predicate' must be set")
