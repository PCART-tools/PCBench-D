    def slice(
        self, offset: int | IntoExprColumn, length: int | IntoExprColumn | None = None
    ) -> Expr:
        """
        Extract a substring from each string value.

        Parameters
        ----------
        offset
            Start index. Negative indexing is supported.
        length
            Length of the slice. If set to `None` (default), the slice is taken to the
            end of the string.

        Returns
        -------
        Expr
            Expression of data type :class:`String`.

        Notes
        -----
        Both the `offset` and `length` inputs are defined in terms of the number
        of characters in the (UTF8) string. A character is defined as a
        `Unicode scalar value`_. A single character is represented by a single byte
        when working with ASCII text, and a maximum of 4 bytes otherwise.

        .. _Unicode scalar value: https://www.unicode.org/glossary/#unicode_scalar_value

        Examples
        --------
        >>> df = pl.DataFrame({"s": ["pear", None, "papaya", "dragonfruit"]})
        >>> df.with_columns(pl.col("s").str.slice(-3).alias("slice"))
        shape: (4, 2)
        ┌─────────────┬───────┐
        │ s           ┆ slice │
        │ ---         ┆ ---   │
        │ str         ┆ str   │
        ╞═════════════╪═══════╡
        │ pear        ┆ ear   │
        │ null        ┆ null  │
        │ papaya      ┆ aya   │
        │ dragonfruit ┆ uit   │
        └─────────────┴───────┘

        Using the optional `length` parameter

        >>> df.with_columns(pl.col("s").str.slice(4, length=3).alias("slice"))
        shape: (4, 2)
        ┌─────────────┬───────┐
        │ s           ┆ slice │
        │ ---         ┆ ---   │
        │ str         ┆ str   │
        ╞═════════════╪═══════╡
        │ pear        ┆       │
        │ null        ┆ null  │
        │ papaya      ┆ ya    │
        │ dragonfruit ┆ onf   │
        └─────────────┴───────┘
        """
        offset = parse_as_expression(offset)
        length = parse_as_expression(length)
        return wrap_expr(self._pyexpr.str_slice(offset, length))
