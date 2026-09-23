    def concat(self, other: list[Expr | str] | Expr | str | Series | list[Any]) -> Expr:
        """
        Concat the arrays in a Series dtype List in linear time.

        Parameters
        ----------
        other
            Columns to concat into a List Series

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "a": [["a"], ["x"]],
        ...         "b": [["b", "c"], ["y", "z"]],
        ...     }
        ... )
        >>> df.with_columns(concat=pl.col("a").list.concat("b"))
        shape: (2, 3)
        ┌───────────┬────────────┬─────────────────┐
        │ a         ┆ b          ┆ concat          │
        │ ---       ┆ ---        ┆ ---             │
        │ list[str] ┆ list[str]  ┆ list[str]       │
        ╞═══════════╪════════════╪═════════════════╡
        │ ["a"]     ┆ ["b", "c"] ┆ ["a", "b", "c"] │
        │ ["x"]     ┆ ["y", "z"] ┆ ["x", "y", "z"] │
        └───────────┴────────────┴─────────────────┘
        """
        if isinstance(other, list) and (
            not isinstance(other[0], (pl.Expr, str, pl.Series))
        ):
            return self.concat(pl.Series([other]))

        other_list: list[Expr | str | Series]
        other_list = [other] if not isinstance(other, list) else copy.copy(other)  # type: ignore[arg-type]

        other_list.insert(0, wrap_expr(self._pyexpr))
        return F.concat_list(other_list)
