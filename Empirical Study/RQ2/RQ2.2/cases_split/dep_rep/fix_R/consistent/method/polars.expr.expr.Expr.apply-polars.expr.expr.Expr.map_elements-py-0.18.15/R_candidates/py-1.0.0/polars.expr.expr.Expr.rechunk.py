    def rechunk(self) -> Expr:
        """
        Create a single chunk of memory for this Series.

        Examples
        --------
        >>> df = pl.DataFrame({"a": [1, 1, 2]})

        Create a Series with 3 nulls, append column a then rechunk

        >>> df.select(pl.repeat(None, 3).append(pl.col("a")).rechunk())
        shape: (6, 1)
        ┌────────┐
        │ repeat │
        │ ---    │
        │ i64    │
        ╞════════╡
        │ null   │
        │ null   │
        │ null   │
        │ 1      │
        │ 1      │
        │ 2      │
        └────────┘
        """
        return self._from_pyexpr(self._pyexpr.rechunk())
