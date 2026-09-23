    def reverse(self) -> Expr:
        """
        Returns string values in reversed order.

        Examples
        --------
        >>> df = pl.DataFrame({"text": ["foo", "bar", "man\u0303ana"]})
        >>> df.with_columns(pl.col("text").str.reverse().alias("reversed"))
        shape: (3, 2)
        ┌────────┬──────────┐
        │ text   ┆ reversed │
        │ ---    ┆ ---      │
        │ str    ┆ str      │
        ╞════════╪══════════╡
        │ foo    ┆ oof      │
        │ bar    ┆ rab      │
        │ mañana ┆ anañam   │
        └────────┴──────────┘
        """
        return wrap_expr(self._pyexpr.str_reverse())
