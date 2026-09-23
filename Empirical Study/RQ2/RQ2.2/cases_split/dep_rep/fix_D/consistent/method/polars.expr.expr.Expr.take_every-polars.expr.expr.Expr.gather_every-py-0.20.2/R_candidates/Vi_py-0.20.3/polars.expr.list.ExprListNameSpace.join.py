    def join(self, separator: IntoExpr) -> Expr:
        """
        Join all string items in a sublist and place a separator between them.

        This errors if inner type of list `!= String`.

        Parameters
        ----------
        separator
            string to separate the items with

        Returns
        -------
        Expr
            Expression of data type :class:`String`.

        Examples
        --------
        >>> df = pl.DataFrame({"s": [["a", "b", "c"], ["x", "y"]]})
        >>> df.with_columns(join=pl.col("s").list.join(" "))
        shape: (2, 2)
        ┌─────────────────┬───────┐
        │ s               ┆ join  │
        │ ---             ┆ ---   │
        │ list[str]       ┆ str   │
        ╞═════════════════╪═══════╡
        │ ["a", "b", "c"] ┆ a b c │
        │ ["x", "y"]      ┆ x y   │
        └─────────────────┴───────┘

        >>> df = pl.DataFrame(
        ...     {"s": [["a", "b", "c"], ["x", "y"]], "separator": ["*", "_"]}
        ... )
        >>> df.with_columns(join=pl.col("s").list.join(pl.col("separator")))
        shape: (2, 3)
        ┌─────────────────┬───────────┬───────┐
        │ s               ┆ separator ┆ join  │
        │ ---             ┆ ---       ┆ ---   │
        │ list[str]       ┆ str       ┆ str   │
        ╞═════════════════╪═══════════╪═══════╡
        │ ["a", "b", "c"] ┆ *         ┆ a*b*c │
        │ ["x", "y"]      ┆ _         ┆ x_y   │
        └─────────────────┴───────────┴───────┘

        """
        separator = parse_as_expression(separator, str_as_lit=True)
        return wrap_expr(self._pyexpr.list_join(separator))
