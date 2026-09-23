    def peak_min(self) -> Expr:
        """
        Get a boolean mask of the local minimum peaks.

        Examples
        --------
        >>> df = pl.DataFrame({"a": [4, 1, 3, 2, 5]})
        >>> df.select(pl.col("a").peak_min())
        shape: (5, 1)
        ┌───────┐
        │ a     │
        │ ---   │
        │ bool  │
        ╞═══════╡
        │ false │
        │ true  │
        │ false │
        │ true  │
        │ false │
        └───────┘
        """
        return self._from_pyexpr(self._pyexpr.peak_min())
