    def median(self) -> Expr:
        """
        Compute the median of the values of the sub-arrays.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     data={"a": [[1, 2], [4, 3]]},
        ...     schema={"a": pl.Array(pl.Int64, 2)},
        ... )
        >>> df.select(pl.col("a").arr.median())
        shape: (2, 1)
        ┌─────┐
        │ a   │
        │ --- │
        │ f64 │
        ╞═════╡
        │ 1.5 │
        │ 3.5 │
        └─────┘
        """
        return wrap_expr(self._pyexpr.arr_median())
