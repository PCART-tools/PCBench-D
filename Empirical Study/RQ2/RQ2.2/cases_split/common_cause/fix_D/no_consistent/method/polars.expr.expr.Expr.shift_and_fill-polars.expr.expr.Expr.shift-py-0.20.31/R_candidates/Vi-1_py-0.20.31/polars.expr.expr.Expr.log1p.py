    def log1p(self) -> Self:
        """
        Compute the natural logarithm of each element plus one.

        This computes `log(1 + x)` but is more numerically stable for `x` close to zero.

        Examples
        --------
        >>> df = pl.DataFrame({"a": [1, 2, 3]})
        >>> df.select(pl.col("a").log1p())
        shape: (3, 1)
        ┌──────────┐
        │ a        │
        │ ---      │
        │ f64      │
        ╞══════════╡
        │ 0.693147 │
        │ 1.098612 │
        │ 1.386294 │
        └──────────┘
        """
        return self._from_pyexpr(self._pyexpr.log1p())
