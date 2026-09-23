    def arctanh(self) -> Expr:
        """
        Compute the element-wise value for the inverse hyperbolic tangent.

        Returns
        -------
        Expr
            Expression of data type :class:`Float64`.

        Examples
        --------
        >>> df = pl.DataFrame({"a": [1.0]})
        >>> df.select(pl.col("a").arctanh())
        shape: (1, 1)
        ┌─────┐
        │ a   │
        │ --- │
        │ f64 │
        ╞═════╡
        │ inf │
        └─────┘
        """
        return self._from_pyexpr(self._pyexpr.arctanh())
