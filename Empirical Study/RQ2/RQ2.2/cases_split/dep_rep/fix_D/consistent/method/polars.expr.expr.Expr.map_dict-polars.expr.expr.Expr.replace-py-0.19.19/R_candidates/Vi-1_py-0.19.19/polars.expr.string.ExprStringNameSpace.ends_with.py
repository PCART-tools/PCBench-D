    def ends_with(self, suffix: str | Expr) -> Expr:
        """
        Check if string values end with a substring.

        Parameters
        ----------
        suffix
            Suffix substring.

        See Also
        --------
        contains : Check if string contains a substring that matches a regex.
        starts_with : Check if string values start with a substring.

        Examples
        --------
        >>> df = pl.DataFrame({"fruits": ["apple", "mango", None]})
        >>> df.with_columns(
        ...     pl.col("fruits").str.ends_with("go").alias("has_suffix"),
        ... )
        shape: (3, 2)
        ┌────────┬────────────┐
        │ fruits ┆ has_suffix │
        │ ---    ┆ ---        │
        │ str    ┆ bool       │
        ╞════════╪════════════╡
        │ apple  ┆ false      │
        │ mango  ┆ true       │
        │ null   ┆ null       │
        └────────┴────────────┘

        >>> df = pl.DataFrame(
        ...     {"fruits": ["apple", "mango", "banana"], "suffix": ["le", "go", "nu"]}
        ... )
        >>> df.with_columns(
        ...     pl.col("fruits").str.ends_with(pl.col("suffix")).alias("has_suffix"),
        ... )
        shape: (3, 3)
        ┌────────┬────────┬────────────┐
        │ fruits ┆ suffix ┆ has_suffix │
        │ ---    ┆ ---    ┆ ---        │
        │ str    ┆ str    ┆ bool       │
        ╞════════╪════════╪════════════╡
        │ apple  ┆ le     ┆ true       │
        │ mango  ┆ go     ┆ true       │
        │ banana ┆ nu     ┆ false      │
        └────────┴────────┴────────────┘

        Using `ends_with` as a filter condition:

        >>> df.filter(pl.col("fruits").str.ends_with("go"))
        shape: (1, 2)
        ┌────────┬────────┐
        │ fruits ┆ suffix │
        │ ---    ┆ ---    │
        │ str    ┆ str    │
        ╞════════╪════════╡
        │ mango  ┆ go     │
        └────────┴────────┘

        """
        suffix = parse_as_expression(suffix, str_as_lit=True)
        return wrap_expr(self._pyexpr.str_ends_with(suffix))
