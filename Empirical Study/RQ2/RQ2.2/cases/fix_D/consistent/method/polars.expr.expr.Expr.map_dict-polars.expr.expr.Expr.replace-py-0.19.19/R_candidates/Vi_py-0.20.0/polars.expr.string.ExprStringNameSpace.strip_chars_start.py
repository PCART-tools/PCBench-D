    def strip_chars_start(self, characters: IntoExprColumn | None = None) -> Expr:
        r"""
        Remove leading characters.

        .. note::
            This method strips any characters present in `characters` from the
            start of the input, no matter their order. To strip a prefix (i.e.
            a "word" of characters in a certain order), use
            :func:`strip_prefix` instead.

        Parameters
        ----------
        characters
            The set of characters to be removed. All combinations of this set of
            characters will be stripped. If set to None (default), all whitespace is
            removed instead.

        See Also
        --------
        strip_prefix
        strip_chars_end

        Examples
        --------
        >>> df = pl.DataFrame({"foo": [" hello ", "\tworld"]})
        >>> df.with_columns(foo_strip_start=pl.col("foo").str.strip_chars_start())
        shape: (2, 2)
        ┌─────────┬─────────────────┐
        │ foo     ┆ foo_strip_start │
        │ ---     ┆ ---             │
        │ str     ┆ str             │
        ╞═════════╪═════════════════╡
        │  hello  ┆ hello           │
        │   world   ┆ world           │
        └─────────┴─────────────────┘

        Characters can be stripped by passing a string as argument. Note that whitespace
        will not be stripped automatically when doing so.

        >>> df.with_columns(
        ...     foo_strip_start=pl.col("foo").str.strip_chars_start("wod\t"),
        ... )
        shape: (2, 2)
        ┌─────────┬─────────────────┐
        │ foo     ┆ foo_strip_start │
        │ ---     ┆ ---             │
        │ str     ┆ str             │
        ╞═════════╪═════════════════╡
        │  hello  ┆  hello          │
        │   world   ┆ rld             │
        └─────────┴─────────────────┘

        The order of the provided characters does not matter, they behave like a set.

        >>> pl.DataFrame({"foo": ["aabcdef"]}).with_columns(
        ...     foo_strip_start=pl.col("foo").str.strip_chars_start("cba")
        ... )
        shape: (1, 2)
        ┌─────────┬─────────────────┐
        │ foo     ┆ foo_strip_start │
        │ ---     ┆ ---             │
        │ str     ┆ str             │
        ╞═════════╪═════════════════╡
        │ aabcdef ┆ def             │
        └─────────┴─────────────────┘

        """
        characters = parse_as_expression(characters, str_as_lit=True)
        return wrap_expr(self._pyexpr.str_strip_chars_start(characters))
