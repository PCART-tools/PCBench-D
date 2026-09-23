    def concat(
        self, delimiter: str | None = None, *, ignore_nulls: bool = True
    ) -> Expr:
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
        if delimiter is None:
            issue_deprecation_warning(
                "The default `delimiter` for `str.concat` will change from '-' to an empty string."
                " Pass a delimiter to silence this warning.",
                version="0.20.5",
            )
            delimiter = "-"
        return wrap_expr(self._pyexpr.str_concat(delimiter, ignore_nulls))
