    def arg_min(self) -> Expr:
        """
        Retrieve the index of the minimal value in every sublist.

        Returns
        -------
        Expr
            Expression of data type :class:`UInt32` or :class:`UInt64`
            (depending on compilation).

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "a": [[1, 2], [2, 1]],
        ...     }
        ... )
        >>> df.with_columns(arg_min=pl.col("a").list.arg_min())
        shape: (2, 2)
        ┌───────────┬─────────┐
        │ a         ┆ arg_min │
        │ ---       ┆ ---     │
        │ list[i64] ┆ u32     │
        ╞═══════════╪═════════╡
        │ [1, 2]    ┆ 0       │
        │ [2, 1]    ┆ 1       │
        └───────────┴─────────┘
        """
        return wrap_expr(self._pyexpr.list_arg_min())
