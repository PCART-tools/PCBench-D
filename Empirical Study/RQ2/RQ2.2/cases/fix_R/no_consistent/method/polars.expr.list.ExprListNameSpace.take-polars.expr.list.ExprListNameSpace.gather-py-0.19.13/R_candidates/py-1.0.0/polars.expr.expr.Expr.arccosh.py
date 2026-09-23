    def arccosh(self) -> Expr:
        """
        Compute the element-wise value for the inverse hyperbolic cosine.

        Returns
        -------
        Expr
            Expression of data type :class:`Float64`.

        Examples
        --------
        >>> df = pl.DataFrame({"a": [1.0]})
        >>> df.select(pl.col("a").arccosh())
        shape: (1, 1)
        ┌─────┐
        │ a   │
        │ --- │
        │ f64 │
        ╞═════╡
        │ 0.0 │
        └─────┘
        """
        return self._from_pyexpr(self._pyexpr.arccosh())
