    def starts_with(self, prefix: str | Expr) -> Expr:
        """
        Check if string values start with a substring.

        Parameters
        ----------
        prefix
            Prefix substring.

        See Also
        --------
        contains : Check if string contains a substring that matches a regex.
        ends_with : Check if string values end with a substring.

        Examples
        --------
        >>> df = pl.DataFrame({"fruits": ["apple", "mango", None]})
        >>> df.with_columns(
        ...     pl.col("fruits").str.starts_with("app").alias("has_prefix"),
        ... )
        shape: (3, 2)
        ┌────────┬────────────┐
        │ fruits ┆ has_prefix │
        │ ---    ┆ ---        │
        │ str    ┆ bool       │
        ╞════════╪════════════╡
        │ apple  ┆ true       │
        │ mango  ┆ false      │
        │ null   ┆ null       │
        └────────┴────────────┘

        >>> df = pl.DataFrame(
        ...     {"fruits": ["apple", "mango", "banana"], "prefix": ["app", "na", "ba"]}
        ... )
        >>> df.with_columns(
        ...     pl.col("fruits").str.starts_with(pl.col("prefix")).alias("has_prefix"),
        ... )
        shape: (3, 3)
        ┌────────┬────────┬────────────┐
        │ fruits ┆ prefix ┆ has_prefix │
        │ ---    ┆ ---    ┆ ---        │
        │ str    ┆ str    ┆ bool       │
        ╞════════╪════════╪════════════╡
        │ apple  ┆ app    ┆ true       │
        │ mango  ┆ na     ┆ false      │
        │ banana ┆ ba     ┆ true       │
        └────────┴────────┴────────────┘

        Using `starts_with` as a filter condition:

        >>> df.filter(pl.col("fruits").str.starts_with("app"))
        shape: (1, 2)
        ┌────────┬────────┐
        │ fruits ┆ prefix │
        │ ---    ┆ ---    │
        │ str    ┆ str    │
        ╞════════╪════════╡
        │ apple  ┆ app    │
        └────────┴────────┘

        """
        prefix = parse_as_expression(prefix, str_as_lit=True)
        return wrap_expr(self._pyexpr.str_starts_with(prefix))
