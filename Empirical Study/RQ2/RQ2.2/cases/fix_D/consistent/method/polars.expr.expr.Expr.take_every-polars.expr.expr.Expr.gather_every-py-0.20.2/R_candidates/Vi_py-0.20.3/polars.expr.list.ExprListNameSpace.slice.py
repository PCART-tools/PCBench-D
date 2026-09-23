    def slice(
        self, offset: int | str | Expr, length: int | str | Expr | None = None
    ) -> Expr:
        """
        Slice every sublist.

        Parameters
        ----------
        offset
            Start index. Negative indexing is supported.
        length
            Length of the slice. If set to `None` (default), the slice is taken to the
            end of the list.

        Examples
        --------
        >>> df = pl.DataFrame({"a": [[1, 2, 3, 4], [10, 2, 1]]})
        >>> df.with_columns(slice=pl.col("a").list.slice(1, 2))
        shape: (2, 2)
        ┌─────────────┬───────────┐
        │ a           ┆ slice     │
        │ ---         ┆ ---       │
        │ list[i64]   ┆ list[i64] │
        ╞═════════════╪═══════════╡
        │ [1, 2, … 4] ┆ [2, 3]    │
        │ [10, 2, 1]  ┆ [2, 1]    │
        └─────────────┴───────────┘

        """
        offset = parse_as_expression(offset)
        length = parse_as_expression(length)
        return wrap_expr(self._pyexpr.list_slice(offset, length))
