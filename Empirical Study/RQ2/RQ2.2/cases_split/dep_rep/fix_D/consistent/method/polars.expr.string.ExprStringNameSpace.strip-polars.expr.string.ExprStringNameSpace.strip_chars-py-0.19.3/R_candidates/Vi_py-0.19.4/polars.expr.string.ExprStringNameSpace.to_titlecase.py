    def to_titlecase(self) -> Expr:
        """
        Transform to titlecase variant.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {"sing": ["welcome to my world", "THERE'S NO TURNING BACK"]}
        ... )
        >>> df.select(pl.col("sing").str.to_titlecase())
        shape: (2, 1)
        ┌─────────────────────────┐
        │ sing                    │
        │ ---                     │
        │ str                     │
        ╞═════════════════════════╡
        │ Welcome To My World     │
        │ There's No Turning Back │
        └─────────────────────────┘

        """
        return wrap_expr(self._pyexpr.str_to_titlecase())
