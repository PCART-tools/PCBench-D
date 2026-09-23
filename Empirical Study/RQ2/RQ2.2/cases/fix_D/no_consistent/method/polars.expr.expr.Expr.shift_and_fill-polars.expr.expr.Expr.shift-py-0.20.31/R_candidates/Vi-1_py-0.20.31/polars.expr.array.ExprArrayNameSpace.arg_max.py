    def arg_max(self) -> Expr:
        """
        Retrieve the index of the maximum value in every sub-array.

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
        >>> df.with_columns(arg_max=pl.col("a").arr.arg_max())
        shape: (2, 2)
        ┌───────────────┬─────────┐
        │ a             ┆ arg_max │
        │ ---           ┆ ---     │
        │ array[i64, 2] ┆ u32     │
        ╞═══════════════╪═════════╡
        │ [1, 2]        ┆ 1       │
        │ [2, 1]        ┆ 0       │
        └───────────────┴─────────┘

        """
        return wrap_expr(self._pyexpr.arr_arg_max())
