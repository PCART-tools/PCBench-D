    def starts_with(self, prefix: bytes | Expr) -> Expr:
        r"""
        Check if values start with a binary substring.

        Parameters
        ----------
        prefix
            Prefix substring.

        Returns
        -------
        Expr
            Expression of data type :class:`Boolean`.

        See Also
        --------
        ends_with : Check if the binary substring exists at the end
        contains : Check if the binary substring exists anywhere

        Examples
        --------
        >>> colors = pl.DataFrame(
        ...     {
        ...         "name": ["black", "yellow", "blue"],
        ...         "code": [b"\x00\x00\x00", b"\xff\xff\x00", b"\x00\x00\xff"],
        ...         "prefix": [b"\x00", b"\xff\x00", b"\x00\x00"],
        ...     }
        ... )
        >>> colors.select(
        ...     "name",
        ...     pl.col("code").bin.starts_with(b"\xff").alias("starts_with_lit"),
        ...     pl.col("code")
        ...     .bin.starts_with(pl.col("prefix"))
        ...     .alias("starts_with_expr"),
        ... )
        shape: (3, 3)
        ┌────────┬─────────────────┬──────────────────┐
        │ name   ┆ starts_with_lit ┆ starts_with_expr │
        │ ---    ┆ ---             ┆ ---              │
        │ str    ┆ bool            ┆ bool             │
        ╞════════╪═════════════════╪══════════════════╡
        │ black  ┆ false           ┆ true             │
        │ yellow ┆ true            ┆ false            │
        │ blue   ┆ false           ┆ true             │
        └────────┴─────────────────┴──────────────────┘
        """
        prefix = parse_as_expression(prefix, str_as_lit=True)
        return wrap_expr(self._pyexpr.bin_starts_with(prefix))
