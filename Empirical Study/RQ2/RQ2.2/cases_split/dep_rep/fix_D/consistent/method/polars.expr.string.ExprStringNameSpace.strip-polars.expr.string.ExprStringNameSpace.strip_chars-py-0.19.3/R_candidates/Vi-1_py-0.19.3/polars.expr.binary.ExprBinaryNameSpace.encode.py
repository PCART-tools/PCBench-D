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
            Expression of data type :class:`Utf8` with values encoded using provided
            encoding.

        Examples
        --------
        >>> colors = pl.DataFrame(
        ...     {
        ...         "name": ["black", "yellow", "blue"],
        ...         "code": [b"\x00\x00\x00", b"\xff\xff\x00", b"\x00\x00\xff"],
        ...     }
        ... )
        >>> colors.with_columns(
        ...     pl.col("code").bin.encode("hex").alias("code_encoded_hex"),
        ... )
        shape: (3, 3)
        ┌────────┬───────────────┬──────────────────┐
        │ name   ┆ code          ┆ code_encoded_hex │
        │ ---    ┆ ---           ┆ ---              │
        │ str    ┆ binary        ┆ str              │
        ╞════════╪═══════════════╪══════════════════╡
        │ black  ┆ [binary data] ┆ 000000           │
        │ yellow ┆ [binary data] ┆ ffff00           │
        │ blue   ┆ [binary data] ┆ 0000ff           │
        └────────┴───────────────┴──────────────────┘

        """
        if encoding == "hex":
            return wrap_expr(self._pyexpr.bin_hex_encode())
        elif encoding == "base64":
            return wrap_expr(self._pyexpr.bin_base64_encode())
        else:
            raise ValueError(
                f"encoding must be one of {{'hex', 'base64'}}, got {encoding!r}"
            )
