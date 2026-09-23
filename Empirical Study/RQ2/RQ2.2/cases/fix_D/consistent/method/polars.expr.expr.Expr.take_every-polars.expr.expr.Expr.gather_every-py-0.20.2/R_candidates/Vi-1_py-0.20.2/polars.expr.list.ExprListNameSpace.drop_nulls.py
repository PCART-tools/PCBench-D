    def drop_nulls(self) -> Expr:
        """
        Drop all null values in the list.

        The original order of the remaining elements is preserved.

        Examples
        --------
        >>> df = pl.DataFrame({"values": [[None, 1, None, 2], [None], [3, 4]]})
        >>> df.with_columns(drop_nulls=pl.col("values").list.drop_nulls())
        shape: (3, 2)
        ┌────────────────┬────────────┐
        │ values         ┆ drop_nulls │
        │ ---            ┆ ---        │
        │ list[i64]      ┆ list[i64]  │
        ╞════════════════╪════════════╡
        │ [null, 1, … 2] ┆ [1, 2]     │
        │ [null]         ┆ []         │
        │ [3, 4]         ┆ [3, 4]     │
        └────────────────┴────────────┘

        """
        return wrap_expr(self._pyexpr.list_drop_nulls())
