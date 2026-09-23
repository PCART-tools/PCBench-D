    def std(self, ddof: int = 1) -> Expr:
        """
        Compute the std of the values of the sub-arrays.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     data={"a": [[1, 2], [4, 3]]},
        ...     schema={"a": pl.Array(pl.Int64, 2)},
        ... )
        >>> df.select(pl.col("a").arr.std())
        shape: (2, 1)
        ┌──────────┐
        │ a        │
        │ ---      │
        │ f64      │
        ╞══════════╡
        │ 0.707107 │
        │ 0.707107 │
        └──────────┘
        """
        return wrap_expr(self._pyexpr.arr_std(ddof))
