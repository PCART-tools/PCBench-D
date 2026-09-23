    def all(self) -> Expr:
        """
        Evaluate whether all boolean values are true for every subarray.

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
        >>> df.with_columns(all=pl.col("a").arr.all())
        shape: (5, 2)
        ┌────────────────┬───────┐
        │ a              ┆ all   │
        │ ---            ┆ ---   │
        │ array[bool, 2] ┆ bool  │
        ╞════════════════╪═══════╡
        │ [true, true]   ┆ true  │
        │ [false, true]  ┆ false │
        │ [false, false] ┆ false │
        │ [null, null]   ┆ true  │
        │ null           ┆ null  │
        └────────────────┴───────┘
        """
        return wrap_expr(self._pyexpr.arr_all())
