    def strip_chars_end(self, characters: IntoExprColumn | None = None) -> Expr:
        r"""
        Remove trailing characters.

        .. note::
            This method strips any characters present in `characters` from the
            end of the input, no matter their order. To strip a suffix (i.e.
            a "word" of characters in a certain order), use
            :func:`strip_suffix` instead.

        Parameters
        ----------
        characters
            The set of characters to be removed. All combinations of this set of
            characters will be stripped from the end of the string. If set to None
            (default), all trailing whitespace is removed instead.

        See Also
        --------
        strip_suffix
        strip_chars_start

        Examples
        --------
        >>> df = pl.DataFrame({"foo": [" hello", "world\n"]})
        >>> df
        shape: (2, 1)
        ┌────────┐
        │ foo    │
        │ ---    │
        │ str    │
        ╞════════╡
        │  hello │
        │ world  │
        │        │
        └────────┘
        >>> df.with_columns(foo_strip_end=pl.col("foo").str.strip_chars_end())
        shape: (2, 2)
        ┌────────┬───────────────┐
        │ foo    ┆ foo_strip_end │
        │ ---    ┆ ---           │
        │ str    ┆ str           │
        ╞════════╪═══════════════╡
        │  hello ┆  hello        │
        │ world  ┆ world         │
        │        ┆               │
        └────────┴───────────────┘

        Characters can be stripped by passing a string as argument. Note that whitespace
        will not be stripped automatically when doing so, unless that whitespace is
        also included in the string.

        >>> df.with_columns(foo_strip_end=pl.col("foo").str.strip_chars_end("oldw "))
        shape: (2, 2)
        ┌────────┬───────────────┐
        │ foo    ┆ foo_strip_end │
        │ ---    ┆ ---           │
        │ str    ┆ str           │
        ╞════════╪═══════════════╡
        │  hello ┆  he           │
        │ world  ┆ world         │
        │        ┆               │
        └────────┴───────────────┘

        The order of the provided characters does not matter, they behave like a set.

        >>> pl.DataFrame({"foo": ["abcdeff"]}).with_columns(
        ...     foo_strip_end=pl.col("foo").str.strip_chars_end("fed")
        ... )
        shape: (1, 2)
        ┌─────────┬───────────────┐
        │ foo     ┆ foo_strip_end │
        │ ---     ┆ ---           │
        │ str     ┆ str           │
        ╞═════════╪═══════════════╡
        │ abcdeff ┆ abc           │
        └─────────┴───────────────┘
        """
        characters = parse_into_expression(characters, str_as_lit=True)
        return wrap_expr(self._pyexpr.str_strip_chars_end(characters))
