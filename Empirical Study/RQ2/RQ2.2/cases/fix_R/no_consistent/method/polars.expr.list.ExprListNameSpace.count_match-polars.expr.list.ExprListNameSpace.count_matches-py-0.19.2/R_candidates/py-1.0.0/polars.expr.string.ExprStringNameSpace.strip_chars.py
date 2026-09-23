    def strip_chars(self, characters: IntoExprColumn | None = None) -> Expr:
        r"""
        Remove leading and trailing characters.

        Parameters
        ----------
        characters
            The set of characters to be removed. All combinations of this set of
            characters will be stripped from the start and end of the string. If set to
            None (default), all leading and trailing whitespace is removed instead.

        Examples
        --------
        >>> df = pl.DataFrame({"foo": [" hello", "\nworld"]})
        >>> df
        shape: (2, 1)
        ┌────────┐
        │ foo    │
        │ ---    │
        │ str    │
        ╞════════╡
        │  hello │
        │        │
        │ world  │
        └────────┘

        >>> df.with_columns(foo_stripped=pl.col("foo").str.strip_chars())
        shape: (2, 2)
        ┌────────┬──────────────┐
        │ foo    ┆ foo_stripped │
        │ ---    ┆ ---          │
        │ str    ┆ str          │
        ╞════════╪══════════════╡
        │  hello ┆ hello        │
        │        ┆ world        │
        │ world  ┆              │
        └────────┴──────────────┘

        Characters can be stripped by passing a string as argument. Note that whitespace
        will not be stripped automatically when doing so, unless that whitespace is
        also included in the string.

        >>> df.with_columns(foo_stripped=pl.col("foo").str.strip_chars("ow\n"))
        shape: (2, 2)
        ┌────────┬──────────────┐
        │ foo    ┆ foo_stripped │
        │ ---    ┆ ---          │
        │ str    ┆ str          │
        ╞════════╪══════════════╡
        │  hello ┆  hell        │
        │        ┆ rld          │
        │ world  ┆              │
        └────────┴──────────────┘
        """
        characters = parse_into_expression(characters, str_as_lit=True)
        return wrap_expr(self._pyexpr.str_strip_chars(characters))
