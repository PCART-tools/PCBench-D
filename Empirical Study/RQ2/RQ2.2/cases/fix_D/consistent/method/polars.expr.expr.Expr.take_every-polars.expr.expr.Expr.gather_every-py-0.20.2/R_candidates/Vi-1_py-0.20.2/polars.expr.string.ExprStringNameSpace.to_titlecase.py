    def to_titlecase(self) -> Expr:
        """
        Transform to titlecase variant.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {"sing": ["welcome to my world", "THERE'S NO TURNING BACK"]}
        ... )
        >>> df.with_columns(foo_title=pl.col("sing").str.to_titlecase())
        shape: (2, 2)
        ┌─────────────────────────┬─────────────────────────┐
        │ sing                    ┆ foo_title               │
        │ ---                     ┆ ---                     │
        │ str                     ┆ str                     │
        ╞═════════════════════════╪═════════════════════════╡
        │ welcome to my world     ┆ Welcome To My World     │
        │ THERE'S NO TURNING BACK ┆ There's No Turning Back │
        └─────────────────────────┴─────────────────────────┘

        """
        return wrap_expr(self._pyexpr.str_to_titlecase())
