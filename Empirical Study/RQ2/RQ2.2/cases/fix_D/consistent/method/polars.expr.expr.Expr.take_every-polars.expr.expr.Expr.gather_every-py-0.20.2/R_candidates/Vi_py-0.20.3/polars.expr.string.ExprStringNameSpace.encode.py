    def encode(self, encoding: TransferEncoding) -> Expr:
        """
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
        >>> df = pl.DataFrame({"strings": ["foo", "bar", None]})
        >>> df.with_columns(strings_hex=pl.col("strings").str.encode("hex"))
        shape: (3, 2)
        ┌─────────┬─────────────┐
        │ strings ┆ strings_hex │
        │ ---     ┆ ---         │
        │ str     ┆ str         │
        ╞═════════╪═════════════╡
        │ foo     ┆ 666f6f      │
        │ bar     ┆ 626172      │
        │ null    ┆ null        │
        └─────────┴─────────────┘

        """
        if encoding == "hex":
            return wrap_expr(self._pyexpr.str_hex_encode())
        elif encoding == "base64":
            return wrap_expr(self._pyexpr.str_base64_encode())
        else:
            raise ValueError(
                f"`encoding` must be one of {{'hex', 'base64'}}, got {encoding!r}"
            )
