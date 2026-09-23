    def degrees(self) -> Expr:
        """
        Convert from radians to degrees.

        Returns
        -------
        Expr
            Expression of data type :class:`Float64`.

        Examples
        --------
        >>> import math
        >>> df = pl.DataFrame({"a": [x * math.pi for x in range(-4, 5)]})
        >>> df.select(pl.col("a").degrees())
        shape: (9, 1)
        ┌────────┐
        │ a      │
        │ ---    │
        │ f64    │
        ╞════════╡
        │ -720.0 │
        │ -540.0 │
        │ -360.0 │
        │ -180.0 │
        │ 0.0    │
        │ 180.0  │
        │ 360.0  │
        │ 540.0  │
        │ 720.0  │
        └────────┘
        """
        return self._from_pyexpr(self._pyexpr.degrees())
