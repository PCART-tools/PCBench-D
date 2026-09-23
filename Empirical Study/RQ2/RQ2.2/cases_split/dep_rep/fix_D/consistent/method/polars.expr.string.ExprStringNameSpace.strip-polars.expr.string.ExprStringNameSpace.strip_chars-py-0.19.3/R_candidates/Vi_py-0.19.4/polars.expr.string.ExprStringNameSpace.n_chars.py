    def n_chars(self) -> Expr:
        """
        Get length of the strings as UInt32 (as number of chars).

        Notes
        -----
        If you know that you are working with ASCII text, ``lengths`` will be
        equivalent, and faster (returns length in terms of the number of bytes).

        Examples
        --------
        >>> df = pl.DataFrame({"s": ["Café", None, "345", "東京"]}).with_columns(
        ...     [
        ...         pl.col("s").str.n_chars().alias("nchars"),
        ...         pl.col("s").str.lengths().alias("length"),
        ...     ]
        ... )
        >>> df
        shape: (4, 3)
        ┌──────┬────────┬────────┐
        │ s    ┆ nchars ┆ length │
        │ ---  ┆ ---    ┆ ---    │
        │ str  ┆ u32    ┆ u32    │
        ╞══════╪════════╪════════╡
        │ Café ┆ 4      ┆ 5      │
        │ null ┆ null   ┆ null   │
        │ 345  ┆ 3      ┆ 3      │
        │ 東京  ┆ 2      ┆ 6      │
        └──────┴────────┴────────┘

        """
        return wrap_expr(self._pyexpr.str_n_chars())
