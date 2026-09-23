    def contains(
        self, pattern: str | Expr, *, literal: bool = False, strict: bool = True
    ) -> Expr:
        """
        Check if string contains a substring that matches a pattern.

        Parameters
        ----------
        pattern
            A valid regular expression pattern, compatible with the `regex crate
            <https://docs.rs/regex/latest/regex/>`_.
        literal
            Treat `pattern` as a literal string, not as a regular expression.
        strict
            Raise an error if the underlying pattern is not a valid regex,
            otherwise mask out with a null value.

        Notes
        -----
        To modify regular expression behaviour (such as case-sensitivity) with
        flags, use the inline `(?iLmsuxU)` syntax. For example:

        >>> pl.DataFrame({"s": ["AAA", "aAa", "aaa"]}).with_columns(
        ...     default_match=pl.col("s").str.contains("AA"),
        ...     insensitive_match=pl.col("s").str.contains("(?i)AA"),
        ... )
        shape: (3, 3)
        ┌─────┬───────────────┬───────────────────┐
        │ s   ┆ default_match ┆ insensitive_match │
        │ --- ┆ ---           ┆ ---               │
        │ str ┆ bool          ┆ bool              │
        ╞═════╪═══════════════╪═══════════════════╡
        │ AAA ┆ true          ┆ true              │
        │ aAa ┆ false         ┆ true              │
        │ aaa ┆ false         ┆ true              │
        └─────┴───────────────┴───────────────────┘

        See the regex crate's section on `grouping and flags
        <https://docs.rs/regex/latest/regex/#grouping-and-flags>`_ for
        additional information about the use of inline expression modifiers.

        See Also
        --------
        starts_with : Check if string values start with a substring.
        ends_with : Check if string values end with a substring.
        find: Return the index of the first substring matching a pattern.

        Examples
        --------
        >>> df = pl.DataFrame({"txt": ["Crab", "cat and dog", "rab$bit", None]})
        >>> df.select(
        ...     pl.col("txt"),
        ...     pl.col("txt").str.contains("cat|bit").alias("regex"),
        ...     pl.col("txt").str.contains("rab$", literal=True).alias("literal"),
        ... )
        shape: (4, 3)
        ┌─────────────┬───────┬─────────┐
        │ txt         ┆ regex ┆ literal │
        │ ---         ┆ ---   ┆ ---     │
        │ str         ┆ bool  ┆ bool    │
        ╞═════════════╪═══════╪═════════╡
        │ Crab        ┆ false ┆ false   │
        │ cat and dog ┆ true  ┆ false   │
        │ rab$bit     ┆ true  ┆ true    │
        │ null        ┆ null  ┆ null    │
        └─────────────┴───────┴─────────┘
        """
        pattern = parse_into_expression(pattern, str_as_lit=True)
        return wrap_expr(self._pyexpr.str_contains(pattern, literal, strict))
