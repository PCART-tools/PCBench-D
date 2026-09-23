    def radians(self) -> Expr:
        """
        Convert from degrees to radians.

        Returns
        -------
        Expr
            Expression of data type :class:`Float64`.

        Examples
        --------
        >>> df = pl.DataFrame({"a": [-720, -540, -360, -180, 0, 180, 360, 540, 720]})
        >>> df.select(pl.col("a").radians())
        shape: (9, 1)
        ┌────────────┐
        │ a          │
        │ ---        │
        │ f64        │
        ╞════════════╡
        │ -12.566371 │
        │ -9.424778  │
        │ -6.283185  │
        │ -3.141593  │
        │ 0.0        │
        │ 3.141593   │
        │ 6.283185   │
        │ 9.424778   │
        │ 12.566371  │
        └────────────┘
        """
        return self._from_pyexpr(self._pyexpr.radians())
