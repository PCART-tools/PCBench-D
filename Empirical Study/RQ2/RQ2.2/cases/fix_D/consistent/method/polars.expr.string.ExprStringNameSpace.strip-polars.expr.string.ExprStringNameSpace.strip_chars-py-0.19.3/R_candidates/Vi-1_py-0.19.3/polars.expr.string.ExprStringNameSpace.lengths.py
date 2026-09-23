    def lengths(self) -> Expr:
        """
        Get length of the strings as UInt32 (as number of bytes).

        Notes
        -----
        The returned lengths are equal to the number of bytes in the UTF8 string. If you
        need the length in terms of the number of characters, use ``n_chars`` instead.

        Examples
        --------
        >>> df = pl.DataFrame({"s": ["Café", None, "345", "東京"]}).with_columns(
        ...     [
        ...         pl.col("s").str.lengths().alias("length"),
        ...         pl.col("s").str.n_chars().alias("nchars"),
        ...     ]
        ... )
        >>> df
        shape: (4, 3)
        ┌──────┬────────┬────────┐
        │ s    ┆ length ┆ nchars │
        │ ---  ┆ ---    ┆ ---    │
        │ str  ┆ u32    ┆ u32    │
        ╞══════╪════════╪════════╡
        │ Café ┆ 5      ┆ 4      │
        │ null ┆ null   ┆ null   │
        │ 345  ┆ 3      ┆ 3      │
        │ 東京  ┆ 6      ┆ 2      │
        └──────┴────────┴────────┘

        """
        return wrap_expr(self._pyexpr.str_lengths())
