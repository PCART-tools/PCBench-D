    def tail(self, n: int | IntoExprColumn) -> Expr:
        """
        Return the last n characters of each string in a String Series.

        Parameters
        ----------
        n
            Length of the slice (integer or expression). Negative indexing is supported;
            see note (2) below.

        Returns
        -------
        Expr
            Expression of data type :class:`String`.

        Notes
        -----
        1) The `n` input is defined in terms of the number of characters in the (UTF8)
           string. A character is defined as a `Unicode scalar value`_. A single
           character is represented by a single byte when working with ASCII text, and a
           maximum of 4 bytes otherwise.

           .. _Unicode scalar value: https://www.unicode.org/glossary/#unicode_scalar_value

        2) When the `n` input is negative, `tail` returns characters starting from the
           `n`th from the beginning of the string. For example, if `n = -3`, then all
           characters except the first three are returned.

        3) If the length of the string has fewer than `n` characters, the full string is
           returned.

        Examples
        --------
        Return up to the last 5 characters:

        >>> df = pl.DataFrame({"s": ["pear", None, "papaya", "dragonfruit"]})
        >>> df.with_columns(pl.col("s").str.tail(5).alias("s_tail_5"))
        shape: (4, 2)
        ┌─────────────┬──────────┐
        │ s           ┆ s_tail_5 │
        │ ---         ┆ ---      │
        │ str         ┆ str      │
        ╞═════════════╪══════════╡
        │ pear        ┆ pear     │
        │ null        ┆ null     │
        │ papaya      ┆ apaya    │
        │ dragonfruit ┆ fruit    │
        └─────────────┴──────────┘

        Return characters determined by column `n`:

        >>> df = pl.DataFrame(
        ...     {
        ...         "s": ["pear", None, "papaya", "dragonfruit"],
        ...         "n": [3, 4, -2, -5],
        ...     }
        ... )
        >>> df.with_columns(pl.col("s").str.tail("n").alias("s_tail_n"))
        shape: (4, 3)
        ┌─────────────┬─────┬──────────┐
        │ s           ┆ n   ┆ s_tail_n │
        │ ---         ┆ --- ┆ ---      │
        │ str         ┆ i64 ┆ str      │
        ╞═════════════╪═════╪══════════╡
        │ pear        ┆ 3   ┆ ear      │
        │ null        ┆ 4   ┆ null     │
        │ papaya      ┆ -2  ┆ paya     │
        │ dragonfruit ┆ -5  ┆ nfruit   │
        └─────────────┴─────┴──────────┘
        """
        n = parse_as_expression(n)
        return wrap_expr(self._pyexpr.str_tail(n))
