    def concat(self, delimiter: str = "-", *, ignore_nulls: bool = True) -> Expr:
        """
        Vertically concat the values in the Series to a single string value.

        Parameters
        ----------
        delimiter
            The delimiter to insert between consecutive string values.
        ignore_nulls
            Ignore null values (default).

            If set to ``False``, null values will be propagated.
            if the column contains any null values, the output is ``None``.

        Returns
        -------
        Expr
            Expression of data type :class:`Utf8`.

        Examples
        --------
        >>> df = pl.DataFrame({"foo": [1, None, 2]})
        >>> df.select(pl.col("foo").str.concat("-"))
        shape: (1, 1)
        ┌─────┐
        │ foo │
        │ --- │
        │ str │
        ╞═════╡
        │ 1-2 │
        └─────┘
        >>> df = pl.DataFrame({"foo": [1, None, 2]})
        >>> df.select(pl.col("foo").str.concat("-", ignore_nulls=False))
        shape: (1, 1)
        ┌──────┐
        │ foo  │
        │ ---  │
        │ str  │
        ╞══════╡
        │ null │
        └──────┘

        """
        return wrap_expr(self._pyexpr.str_concat(delimiter, ignore_nulls))
