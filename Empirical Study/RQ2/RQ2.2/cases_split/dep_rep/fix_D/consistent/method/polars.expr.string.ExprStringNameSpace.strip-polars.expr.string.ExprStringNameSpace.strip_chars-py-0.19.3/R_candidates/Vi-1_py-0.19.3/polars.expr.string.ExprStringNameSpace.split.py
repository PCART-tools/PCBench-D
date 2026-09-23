    def split(self, by: str | Expr, *, inclusive: bool = False) -> Expr:
        """
        Split the string by a substring.

        Parameters
        ----------
        by
            Substring to split by.
        inclusive
            If True, include the split character/string in the results.

        Examples
        --------
        >>> df = pl.DataFrame({"s": ["foo bar", "foo_bar", "foo_bar_baz"]})
        >>> df.with_columns(
        ...     pl.col("s").str.split(by="_").alias("split"),
        ...     pl.col("s").str.split(by="_", inclusive=True).alias("split_inclusive"),
        ... )
        shape: (3, 3)
        ┌─────────────┬───────────────────────┬─────────────────────────┐
        │ s           ┆ split                 ┆ split_inclusive         │
        │ ---         ┆ ---                   ┆ ---                     │
        │ str         ┆ list[str]             ┆ list[str]               │
        ╞═════════════╪═══════════════════════╪═════════════════════════╡
        │ foo bar     ┆ ["foo bar"]           ┆ ["foo bar"]             │
        │ foo_bar     ┆ ["foo", "bar"]        ┆ ["foo_", "bar"]         │
        │ foo_bar_baz ┆ ["foo", "bar", "baz"] ┆ ["foo_", "bar_", "baz"] │
        └─────────────┴───────────────────────┴─────────────────────────┘

        >>> df = pl.DataFrame(
        ...     {"s": ["foo^bar", "foo_bar", "foo*bar*baz"], "by": ["_", "_", "*"]}
        ... )
        >>> df.with_columns(
        ...     pl.col("s").str.split(by=pl.col("by")).alias("split"),
        ...     pl.col("s")
        ...     .str.split(by=pl.col("by"), inclusive=True)
        ...     .alias("split_inclusive"),
        ... )
        shape: (3, 4)
        ┌─────────────┬─────┬───────────────────────┬─────────────────────────┐
        │ s           ┆ by  ┆ split                 ┆ split_inclusive         │
        │ ---         ┆ --- ┆ ---                   ┆ ---                     │
        │ str         ┆ str ┆ list[str]             ┆ list[str]               │
        ╞═════════════╪═════╪═══════════════════════╪═════════════════════════╡
        │ foo^bar     ┆ _   ┆ ["foo^bar"]           ┆ ["foo^bar"]             │
        │ foo_bar     ┆ _   ┆ ["foo", "bar"]        ┆ ["foo_", "bar"]         │
        │ foo*bar*baz ┆ *   ┆ ["foo", "bar", "baz"] ┆ ["foo*", "bar*", "baz"] │
        └─────────────┴─────┴───────────────────────┴─────────────────────────┘

        Returns
        -------
        Expr
            Expression of data type :class:`Utf8`.

        """
        by = parse_as_expression(by, str_as_lit=True)
        if inclusive:
            return wrap_expr(self._pyexpr.str_split_inclusive(by))
        return wrap_expr(self._pyexpr.str_split(by))
