    def count_matches(self, element: IntoExpr) -> Expr:
        """
        Count how often the value produced by ``element`` occurs.

        Parameters
        ----------
        element
            An expression that produces a single value

        Examples
        --------
        >>> df = pl.DataFrame({"listcol": [[0], [1], [1, 2, 3, 2], [1, 2, 1], [4, 4]]})
        >>> df.select(pl.col("listcol").list.count_matches(2).alias("number_of_twos"))
        shape: (5, 1)
        ┌────────────────┐
        │ number_of_twos │
        │ ---            │
        │ u32            │
        ╞════════════════╡
        │ 0              │
        │ 0              │
        │ 2              │
        │ 1              │
        │ 0              │
        └────────────────┘

        """
        element = parse_as_expression(element, str_as_lit=True)
        return wrap_expr(self._pyexpr.list_count_matches(element))
