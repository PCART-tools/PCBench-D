    def ends_with(self, suffix: bytes | Expr) -> Expr:
        r"""
        Check if string values end with a binary substring.

        Parameters
        ----------
        suffix
            Suffix substring.

        Returns
        -------
        Expr
            Expression of data type :class:`Boolean`.

        See Also
        --------
        starts_with : Check if the binary substring exists at the start
        contains : Check if the binary substring exists anywhere

        Examples
        --------
        >>> colors = pl.DataFrame(
        ...     {
        ...         "name": ["black", "yellow", "blue"],
        ...         "code": [b"\x00\x00\x00", b"\xff\xff\x00", b"\x00\x00\xff"],
        ...         "suffix": [b"\x00", b"\xff\x00", b"\x00\x00"],
        ...     }
        ... )
        >>> colors.select(
        ...     "name",
        ...     pl.col("code").bin.ends_with(b"\xff").alias("ends_with_lit"),
        ...     pl.col("code").bin.ends_with(pl.col("suffix")).alias("ends_with_expr"),
        ... )
        shape: (3, 3)
        ┌────────┬───────────────┬────────────────┐
        │ name   ┆ ends_with_lit ┆ ends_with_expr │
        │ ---    ┆ ---           ┆ ---            │
        │ str    ┆ bool          ┆ bool           │
        ╞════════╪═══════════════╪════════════════╡
        │ black  ┆ false         ┆ true           │
        │ yellow ┆ false         ┆ true           │
        │ blue   ┆ true          ┆ false          │
        └────────┴───────────────┴────────────────┘
        """
        suffix = parse_as_expression(suffix, str_as_lit=True)
        return wrap_expr(self._pyexpr.bin_ends_with(suffix))
