    def decode(self, encoding: TransferEncoding, *, strict: bool = True) -> Expr:
        r"""
        Decode values using the provided encoding.

        Parameters
        ----------
        encoding : {'hex', 'base64'}
            The encoding to use.
        strict
            Raise an error if the underlying value cannot be decoded,
            otherwise mask out with a null value.

        Returns
        -------
        Expr
            Expression of data type :class:`Binary`.

        Examples
        --------
        >>> df = pl.DataFrame({"color": ["000000", "ffff00", "0000ff"]})
        >>> df.with_columns(pl.col("color").str.decode("hex").alias("decoded"))
        shape: (3, 2)
        ┌────────┬─────────────────┐
        │ color  ┆ decoded         │
        │ ---    ┆ ---             │
        │ str    ┆ binary          │
        ╞════════╪═════════════════╡
        │ 000000 ┆ b"\x00\x00\x00" │
        │ ffff00 ┆ b"\xff\xff\x00" │
        │ 0000ff ┆ b"\x00\x00\xff" │
        └────────┴─────────────────┘
        """
        if encoding == "hex":
            return wrap_expr(self._pyexpr.str_hex_decode(strict))
        elif encoding == "base64":
            return wrap_expr(self._pyexpr.str_base64_decode(strict))
        else:
            msg = f"`encoding` must be one of {{'hex', 'base64'}}, got {encoding!r}"
            raise ValueError(msg)
