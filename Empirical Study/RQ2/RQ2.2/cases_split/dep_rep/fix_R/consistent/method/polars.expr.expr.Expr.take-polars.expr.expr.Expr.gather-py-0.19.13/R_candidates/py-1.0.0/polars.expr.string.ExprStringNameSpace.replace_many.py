    def replace_many(
        self,
        patterns: IntoExpr,
        replace_with: IntoExpr,
        *,
        ascii_case_insensitive: bool = False,
    ) -> Expr:
        """

        Use the aho-corasick algorithm to replace many matches.

        Parameters
        ----------
        patterns
            String patterns to search and replace.
        replace_with
            Strings to replace where a pattern was a match.
            This can be broadcasted. So it supports many:one and many:many.
        ascii_case_insensitive
            Enable ASCII-aware case insensitive matching.
            When this option is enabled, searching will be performed without respect
            to case for ASCII letters (a-z and A-Z) only.

        Examples
        --------
        >>> _ = pl.Config.set_fmt_str_lengths(100)
        >>> df = pl.DataFrame(
        ...     {
        ...         "lyrics": [
        ...             "Everybody wants to rule the world",
        ...             "Tell me what you want, what you really really want",
        ...             "Can you feel the love tonight",
        ...         ]
        ...     }
        ... )
        >>> df.with_columns(
        ...     pl.col("lyrics")
        ...     .str.replace_many(
        ...         ["me", "you", "they"],
        ...         "",
        ...     )
        ...     .alias("removes_pronouns")
        ... )
        shape: (3, 2)
        ┌────────────────────────────────────────────────────┬────────────────────────────────────────────┐
        │ lyrics                                             ┆ removes_pronouns                           │
        │ ---                                                ┆ ---                                        │
        │ str                                                ┆ str                                        │
        ╞════════════════════════════════════════════════════╪════════════════════════════════════════════╡
        │ Everybody wants to rule the world                  ┆ Everybody wants to rule the world          │
        │ Tell me what you want, what you really really want ┆ Tell  what  want, what  really really want │
        │ Can you feel the love tonight                      ┆ Can  feel the love tonight                 │
        └────────────────────────────────────────────────────┴────────────────────────────────────────────┘
        >>> df.with_columns(
        ...     pl.col("lyrics")
        ...     .str.replace_many(
        ...         ["me", "you"],
        ...         ["you", "me"],
        ...     )
        ...     .alias("confusing")
        ... )  # doctest: +IGNORE_RESULT
        shape: (3, 2)
        ┌────────────────────────────────────────────────────┬───────────────────────────────────────────────────┐
        │ lyrics                                             ┆ confusing                                         │
        │ ---                                                ┆ ---                                               │
        │ str                                                ┆ str                                               │
        ╞════════════════════════════════════════════════════╪═══════════════════════════════════════════════════╡
        │ Everybody wants to rule the world                  ┆ Everybody wants to rule the world                 │
        │ Tell me what you want, what you really really want ┆ Tell you what me want, what me really really want │
        │ Can you feel the love tonight                      ┆ Can me feel the love tonight                      │
        └────────────────────────────────────────────────────┴───────────────────────────────────────────────────┘
        """  # noqa: W505
        patterns = parse_into_expression(
            patterns, str_as_lit=False, list_as_series=True
        )
        replace_with = parse_into_expression(
            replace_with, str_as_lit=True, list_as_series=True
        )
        return wrap_expr(
            self._pyexpr.str_replace_many(
                patterns, replace_with, ascii_case_insensitive
            )
        )
