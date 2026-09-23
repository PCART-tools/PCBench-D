    def contains(self, literal: IntoExpr) -> Expr:
        r"""
        Check if binaries in Series contain a binary substring.

        Parameters
        ----------
        literal
            The binary substring to look for

        Returns
        -------
        Expr
            Expression of data type :class:`Boolean`.

        See Also
        --------
        starts_with : Check if the binary substring exists at the start
        ends_with : Check if the binary substring exists at the end

        Examples
        --------
        >>> colors = pl.DataFrame(
        ...     {
        ...         "name": ["black", "yellow", "blue"],
        ...         "code": [b"\x00\x00\x00", b"\xff\xff\x00", b"\x00\x00\xff"],
        ...         "lit": [b"\x00", b"\xff\x00", b"\xff\xff"],
        ...     }
        ... )
        >>> colors.select(
        ...     "name",
        ...     pl.col("code").bin.contains(b"\xff").alias("contains_with_lit"),
        ...     pl.col("code").bin.contains(pl.col("lit")).alias("contains_with_expr"),
        ... )
        shape: (3, 3)
        ┌────────┬───────────────────┬────────────────────┐
        │ name   ┆ contains_with_lit ┆ contains_with_expr │
        │ ---    ┆ ---               ┆ ---                │
        │ str    ┆ bool              ┆ bool               │
        ╞════════╪═══════════════════╪════════════════════╡
        │ black  ┆ false             ┆ true               │
        │ yellow ┆ true              ┆ true               │
        │ blue   ┆ true              ┆ false              │
        └────────┴───────────────────┴────────────────────┘
        """
        literal = parse_into_expression(literal, str_as_lit=True)
        return wrap_expr(self._pyexpr.bin_contains(literal))
