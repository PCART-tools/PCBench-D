    def join(self, delimiter: str = "", *, ignore_nulls: bool = True) -> Expr:
        """
        Vertically concatenate the string values in the column to a single string value.

        Parameters
        ----------
        delimiter
            The delimiter to insert between consecutive string values.
        ignore_nulls
            Ignore null values (default).
            If set to `False`, null values will be propagated. This means that
            if the column contains any null values, the output is null.

        Returns
        -------
        Expr
            Expression of data type :class:`String`.

        Examples
        --------
        >>> df = pl.DataFrame({"foo": [1, None, 3]})
        >>> df.select(pl.col("foo").str.join("-"))
        shape: (1, 1)
        ┌─────┐
        │ foo │
        │ --- │
        │ str │
        ╞═════╡
        │ 1-3 │
        └─────┘
        >>> df.select(pl.col("foo").str.join(ignore_nulls=False))
        shape: (1, 1)
        ┌──────┐
        │ foo  │
        │ ---  │
        │ str  │
        ╞══════╡
        │ null │
        └──────┘
        """
        return wrap_expr(self._pyexpr.str_join(delimiter, ignore_nulls=ignore_nulls))
