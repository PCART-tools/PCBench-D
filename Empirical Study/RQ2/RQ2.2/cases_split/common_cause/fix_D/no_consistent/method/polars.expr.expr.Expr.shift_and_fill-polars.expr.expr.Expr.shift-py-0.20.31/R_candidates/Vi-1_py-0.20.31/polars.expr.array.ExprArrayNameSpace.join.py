    def join(self, separator: IntoExprColumn, *, ignore_nulls: bool = True) -> Expr:
        """
        Join all string items in a sub-array and place a separator between them.

        This errors if inner type of array `!= String`.

        Parameters
        ----------
        separator
            string to separate the items with
        ignore_nulls
            Ignore null values (default).

            If set to ``False``, null values will be propagated.
            If the sub-list contains any null values, the output is ``None``.

        Returns
        -------
        Expr
            Expression of data type :class:`String`.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {"s": [["a", "b"], ["x", "y"]], "separator": ["*", "_"]},
        ...     schema={
        ...         "s": pl.Array(pl.String, 2),
        ...         "separator": pl.String,
        ...     },
        ... )
        >>> df.with_columns(join=pl.col("s").arr.join(pl.col("separator")))
        shape: (2, 3)
        ┌───────────────┬───────────┬──────┐
        │ s             ┆ separator ┆ join │
        │ ---           ┆ ---       ┆ ---  │
        │ array[str, 2] ┆ str       ┆ str  │
        ╞═══════════════╪═══════════╪══════╡
        │ ["a", "b"]    ┆ *         ┆ a*b  │
        │ ["x", "y"]    ┆ _         ┆ x_y  │
        └───────────────┴───────────┴──────┘

        """
        separator = parse_as_expression(separator, str_as_lit=True)
        return wrap_expr(self._pyexpr.arr_join(separator, ignore_nulls))
