    def peak_max(self) -> Self:
        """
        Get a boolean mask of the local maximum peaks.

        Examples
        --------
        >>> df = pl.DataFrame({"a": [1, 2, 3, 4, 5]})
        >>> df.select(pl.col("a").peak_max())
        shape: (5, 1)
        ┌───────┐
        │ a     │
        │ ---   │
        │ bool  │
        ╞═══════╡
        │ false │
        │ false │
        │ false │
        │ false │
        │ true  │
        └───────┘
        """
        return self._from_pyexpr(self._pyexpr.peak_max())
