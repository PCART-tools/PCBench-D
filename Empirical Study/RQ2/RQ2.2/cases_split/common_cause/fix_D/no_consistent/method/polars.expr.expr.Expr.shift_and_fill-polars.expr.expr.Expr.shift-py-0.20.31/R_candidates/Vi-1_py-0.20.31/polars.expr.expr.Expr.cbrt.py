    def cbrt(self) -> Self:
        """
        Compute the cube root of the elements.

        Examples
        --------
        >>> df = pl.DataFrame({"values": [1.0, 2.0, 4.0]})
        >>> df.select(pl.col("values").cbrt())
        shape: (3, 1)
        ┌──────────┐
        │ values   │
        │ ---      │
        │ f64      │
        ╞══════════╡
        │ 1.0      │
        │ 1.259921 │
        │ 1.587401 │
        └──────────┘
        """
        return self._from_pyexpr(self._pyexpr.cbrt())
