    def count_matches(self, element: IntoExpr) -> Expr:
        """
        Count how often the value produced by `element` occurs.

        Parameters
        ----------
        element
            An expression that produces a single value

        Examples
        --------
        >>> df = pl.DataFrame({"a": [[0], [1], [1, 2, 3, 2], [1, 2, 1], [4, 4]]})
        >>> df.with_columns(number_of_twos=pl.col("a").list.count_matches(2))
        shape: (5, 2)
        ┌─────────────┬────────────────┐
        │ a           ┆ number_of_twos │
        │ ---         ┆ ---            │
        │ list[i64]   ┆ u32            │
        ╞═════════════╪════════════════╡
        │ [0]         ┆ 0              │
        │ [1]         ┆ 0              │
        │ [1, 2, … 2] ┆ 2              │
        │ [1, 2, 1]   ┆ 1              │
        │ [4, 4]      ┆ 0              │
        └─────────────┴────────────────┘

        """
        element = parse_as_expression(element, str_as_lit=True)
        return wrap_expr(self._pyexpr.list_count_matches(element))
