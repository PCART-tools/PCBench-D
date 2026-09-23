    def count_matches(self, element: IntoExpr) -> Expr:
        """
        Count how often the value produced by `element` occurs.

        Parameters
        ----------
        element
            An expression that produces a single value

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {"a": [[1, 2], [1, 1], [2, 2]]}, schema={"a": pl.Array(pl.Int64, 2)}
        ... )
        >>> df.with_columns(number_of_twos=pl.col("a").arr.count_matches(2))
        shape: (3, 2)
        ┌───────────────┬────────────────┐
        │ a             ┆ number_of_twos │
        │ ---           ┆ ---            │
        │ array[i64, 2] ┆ u32            │
        ╞═══════════════╪════════════════╡
        │ [1, 2]        ┆ 1              │
        │ [1, 1]        ┆ 0              │
        │ [2, 2]        ┆ 2              │
        └───────────────┴────────────────┘
        """
        element = parse_into_expression(element, str_as_lit=True)
        return wrap_expr(self._pyexpr.arr_count_matches(element))
