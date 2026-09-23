    def encode(self, encoding: TransferEncoding) -> Expr:
        r"""
        Encode a value using the provided encoding.

        Parameters
        ----------
        encoding : {'hex', 'base64'}
            The encoding to use.

        Returns
        -------
        Expr
            Expression of data type :class:`String`.

        Examples
        --------
        >>> colors = pl.DataFrame(
        ...     {
        ...         "color": ["black", "yellow", "blue"],
        ...         "code": [b"\x00\x00\x00", b"\xff\xff\x00", b"\x00\x00\xff"],
        ...     }
        ... )
        >>> colors.with_columns(
        ...     pl.col("code").bin.encode("hex").alias("encoded"),
        ... )
        shape: (3, 3)
        ┌────────┬─────────────────┬─────────┐
        │ color  ┆ code            ┆ encoded │
        │ ---    ┆ ---             ┆ ---     │
        │ str    ┆ binary          ┆ str     │
        ╞════════╪═════════════════╪═════════╡
        │ black  ┆ b"\x00\x00\x00" ┆ 000000  │
        │ yellow ┆ b"\xff\xff\x00" ┆ ffff00  │
        │ blue   ┆ b"\x00\x00\xff" ┆ 0000ff  │
        └────────┴─────────────────┴─────────┘
        """
        if encoding == "hex":
            return wrap_expr(self._pyexpr.bin_hex_encode())
        elif encoding == "base64":
            return wrap_expr(self._pyexpr.bin_base64_encode())
        else:
            msg = f"`encoding` must be one of {{'hex', 'base64'}}, got {encoding!r}"
            raise ValueError(msg)
