    def arg_min(self) -> Expr:
        """
        Retrieve the index of the minimal value in every sub-array.

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
        ...     },
        ...     schema={"a": pl.Array(pl.Int64, 2)},
        ... )
        >>> df.with_columns(arg_min=pl.col("a").arr.arg_min())
        shape: (2, 2)
        ┌───────────────┬─────────┐
        │ a             ┆ arg_min │
        │ ---           ┆ ---     │
        │ array[i64, 2] ┆ u32     │
        ╞═══════════════╪═════════╡
        │ [1, 2]        ┆ 0       │
        │ [2, 1]        ┆ 1       │
        └───────────────┴─────────┘

        """
        return wrap_expr(self._pyexpr.arr_arg_min())
