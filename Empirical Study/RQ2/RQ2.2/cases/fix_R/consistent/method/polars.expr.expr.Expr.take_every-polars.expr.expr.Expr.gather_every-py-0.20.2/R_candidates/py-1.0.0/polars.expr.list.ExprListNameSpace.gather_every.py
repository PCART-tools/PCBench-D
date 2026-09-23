    def gather_every(
        self,
        n: int | IntoExprColumn,
        offset: int | IntoExprColumn = 0,
    ) -> Expr:
        """
        Take every n-th value start from offset in sublists.

        Parameters
        ----------
        n
            Gather every n-th element.
        offset
            Starting index.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "a": [[1, 2, 3, 4, 5], [6, 7, 8], [9, 10, 11, 12]],
        ...         "n": [2, 1, 3],
        ...         "offset": [0, 1, 0],
        ...     }
        ... )
        >>> df.with_columns(
        ...     gather_every=pl.col("a").list.gather_every(
        ...         n=pl.col("n"), offset=pl.col("offset")
        ...     )
        ... )
        shape: (3, 4)
        ┌───────────────┬─────┬────────┬──────────────┐
        │ a             ┆ n   ┆ offset ┆ gather_every │
        │ ---           ┆ --- ┆ ---    ┆ ---          │
        │ list[i64]     ┆ i64 ┆ i64    ┆ list[i64]    │
        ╞═══════════════╪═════╪════════╪══════════════╡
        │ [1, 2, … 5]   ┆ 2   ┆ 0      ┆ [1, 3, 5]    │
        │ [6, 7, 8]     ┆ 1   ┆ 1      ┆ [7, 8]       │
        │ [9, 10, … 12] ┆ 3   ┆ 0      ┆ [9, 12]      │
        └───────────────┴─────┴────────┴──────────────┘
        """
        n = parse_into_expression(n)
        offset = parse_into_expression(offset)
        return wrap_expr(self._pyexpr.list_gather_every(n, offset))
