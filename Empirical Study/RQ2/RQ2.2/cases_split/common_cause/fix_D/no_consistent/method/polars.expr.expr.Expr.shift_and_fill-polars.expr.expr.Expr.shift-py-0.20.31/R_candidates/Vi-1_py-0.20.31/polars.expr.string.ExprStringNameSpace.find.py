    def find(
        self, pattern: str | Expr, *, literal: bool = False, strict: bool = True
    ) -> Expr:
        """
        Return the index position of the first substring matching a pattern.

        If the pattern is not found, returns None.

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
        ...     default_match=pl.col("s").str.find("Aa"),
        ...     insensitive_match=pl.col("s").str.find("(?i)Aa"),
        ... )
        shape: (3, 3)
        ┌─────┬───────────────┬───────────────────┐
        │ s   ┆ default_match ┆ insensitive_match │
        │ --- ┆ ---           ┆ ---               │
        │ str ┆ u32           ┆ u32               │
        ╞═════╪═══════════════╪═══════════════════╡
        │ AAA ┆ null          ┆ 0                 │
        │ aAa ┆ 1             ┆ 0                 │
        │ aaa ┆ null          ┆ 0                 │
        └─────┴───────────────┴───────────────────┘

        See the regex crate's section on `grouping and flags
        <https://docs.rs/regex/latest/regex/#grouping-and-flags>`_ for
        additional information about the use of inline expression modifiers.

        See Also
        --------
        contains : Check if string contains a substring that matches a regex.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "txt": ["Crab", "Lobster", None, "Crustaceon"],
        ...         "pat": ["a[bc]", "b.t", "[aeiuo]", "(?i)A[BC]"],
        ...     }
        ... )

        Find the index of the first substring matching a regex or literal pattern:

        >>> df.select(
        ...     pl.col("txt"),
        ...     pl.col("txt").str.find("a|e").alias("a|e (regex)"),
        ...     pl.col("txt").str.find("e", literal=True).alias("e (lit)"),
        ... )
        shape: (4, 3)
        ┌────────────┬─────────────┬─────────┐
        │ txt        ┆ a|e (regex) ┆ e (lit) │
        │ ---        ┆ ---         ┆ ---     │
        │ str        ┆ u32         ┆ u32     │
        ╞════════════╪═════════════╪═════════╡
        │ Crab       ┆ 2           ┆ null    │
        │ Lobster    ┆ 5           ┆ 5       │
        │ null       ┆ null        ┆ null    │
        │ Crustaceon ┆ 5           ┆ 7       │
        └────────────┴─────────────┴─────────┘

        Match against a pattern found in another column or (expression):

        >>> df.with_columns(pl.col("txt").str.find(pl.col("pat")).alias("find_pat"))
        shape: (4, 3)
        ┌────────────┬───────────┬──────────┐
        │ txt        ┆ pat       ┆ find_pat │
        │ ---        ┆ ---       ┆ ---      │
        │ str        ┆ str       ┆ u32      │
        ╞════════════╪═══════════╪══════════╡
        │ Crab       ┆ a[bc]     ┆ 2        │
        │ Lobster    ┆ b.t       ┆ 2        │
        │ null       ┆ [aeiuo]   ┆ null     │
        │ Crustaceon ┆ (?i)A[BC] ┆ 5        │
        └────────────┴───────────┴──────────┘
        """
        pattern = parse_as_expression(pattern, str_as_lit=True)
        return wrap_expr(self._pyexpr.str_find(pattern, literal, strict))
