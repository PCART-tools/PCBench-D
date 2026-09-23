    def max(self) -> Expr:
        """
        Get maximum value.

        Examples
        --------
        >>> df = pl.DataFrame({"a": [-1.0, float("nan"), 1.0]})
        >>> df.select(pl.col("a").max())
        shape: (1, 1)
        ┌─────┐
        │ a   │
        │ --- │
        │ f64 │
        ╞═════╡
        │ 1.0 │
        └─────┘
        """
        return self._from_pyexpr(self._pyexpr.max())
