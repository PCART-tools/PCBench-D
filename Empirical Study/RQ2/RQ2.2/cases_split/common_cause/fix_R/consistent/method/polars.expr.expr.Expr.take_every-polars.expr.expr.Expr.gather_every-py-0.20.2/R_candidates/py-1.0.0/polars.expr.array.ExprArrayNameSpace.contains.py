    def contains(
        self, item: float | str | bool | int | date | datetime | time | IntoExprColumn
    ) -> Expr:
        """
        Check if sub-arrays contain the given item.

        Parameters
        ----------
        item
            Item that will be checked for membership

        Returns
        -------
        Expr
            Expression of data type :class:`Boolean`.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {"a": [["a", "b"], ["x", "y"], ["a", "c"]]},
        ...     schema={"a": pl.Array(pl.String, 2)},
        ... )
        >>> df.with_columns(contains=pl.col("a").arr.contains("a"))
        shape: (3, 2)
        ┌───────────────┬──────────┐
        │ a             ┆ contains │
        │ ---           ┆ ---      │
        │ array[str, 2] ┆ bool     │
        ╞═══════════════╪══════════╡
        │ ["a", "b"]    ┆ true     │
        │ ["x", "y"]    ┆ false    │
        │ ["a", "c"]    ┆ true     │
        └───────────────┴──────────┘

        """
        item = parse_into_expression(item, str_as_lit=True)
        return wrap_expr(self._pyexpr.arr_contains(item))
