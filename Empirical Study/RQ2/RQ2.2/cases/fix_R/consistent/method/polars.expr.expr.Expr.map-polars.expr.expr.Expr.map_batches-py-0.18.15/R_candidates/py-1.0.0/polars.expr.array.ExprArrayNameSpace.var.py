    def var(self, ddof: int = 1) -> Expr:
        """
        Compute the var of the values of the sub-arrays.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     data={"a": [[1, 2], [4, 3]]},
        ...     schema={"a": pl.Array(pl.Int64, 2)},
        ... )
        >>> df.select(pl.col("a").arr.var())
        shape: (2, 1)
        ┌─────┐
        │ a   │
        │ --- │
        │ f64 │
        ╞═════╡
        │ 0.5 │
        │ 0.5 │
        └─────┘
        """
        return wrap_expr(self._pyexpr.arr_var(ddof))
