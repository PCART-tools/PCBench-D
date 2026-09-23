    def cot(self) -> Self:
        """
        Compute the element-wise value for the cotangent.

        Returns
        -------
        Expr
            Expression of data type :class:`Float64`.

        Examples
        --------
        >>> df = pl.DataFrame({"a": [1.0]})
        >>> df.select(pl.col("a").cot().round(2))
        shape: (1, 1)
        ┌──────┐
        │ a    │
        │ ---  │
        │ f64  │
        ╞══════╡
        │ 0.64 │
        └──────┘
        """
        return self._from_pyexpr(self._pyexpr.cot())
