    def any(self) -> Expr:
        """
        Evaluate whether any boolean value is true for every subarray.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     data={
        ...         "a": [
        ...             [True, True],
        ...             [False, True],
        ...             [False, False],
        ...             [None, None],
        ...             None,
        ...         ]
        ...     },
        ...     schema={"a": pl.Array(pl.Boolean, 2)},
        ... )
        >>> df.with_columns(any=pl.col("a").arr.any())
        shape: (5, 2)
        ┌────────────────┬───────┐
        │ a              ┆ any   │
        │ ---            ┆ ---   │
        │ array[bool, 2] ┆ bool  │
        ╞════════════════╪═══════╡
        │ [true, true]   ┆ true  │
        │ [false, true]  ┆ true  │
        │ [false, false] ┆ false │
        │ [null, null]   ┆ false │
        │ null           ┆ null  │
        └────────────────┴───────┘
        """
        return wrap_expr(self._pyexpr.arr_any())
