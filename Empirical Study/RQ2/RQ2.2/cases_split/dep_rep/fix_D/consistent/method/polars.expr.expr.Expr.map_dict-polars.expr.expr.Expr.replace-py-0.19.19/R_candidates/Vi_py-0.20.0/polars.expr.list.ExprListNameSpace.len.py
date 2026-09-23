    def len(self) -> Expr:
        """
        Return the number of elements in each list.

        Null values count towards the total.

        Returns
        -------
        Expr
            Expression of data type :class:`UInt32`.

        Examples
        --------
        >>> df = pl.DataFrame({"a": [[1, 2, None], [5]]})
        >>> df.with_columns(len=pl.col("a").list.len())
        shape: (2, 2)
        ┌──────────────┬─────┐
        │ a            ┆ len │
        │ ---          ┆ --- │
        │ list[i64]    ┆ u32 │
        ╞══════════════╪═════╡
        │ [1, 2, null] ┆ 3   │
        │ [5]          ┆ 1   │
        └──────────────┴─────┘

        """
        return wrap_expr(self._pyexpr.list_len())
