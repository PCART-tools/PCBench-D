    def contains_any(
        self, patterns: IntoExpr, *, ascii_case_insensitive: bool = False
    ) -> Expr:
        """
        Use the aho-corasick algorithm to find matches.

        This version determines if any of the patterns find a match.

        Parameters
        ----------
        patterns
            String patterns to search.
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
        ...     pl.col("lyrics").str.contains_any(["you", "me"]).alias("contains_any")
        ... )
        shape: (3, 2)
        ┌────────────────────────────────────────────────────┬──────────────┐
        │ lyrics                                             ┆ contains_any │
        │ ---                                                ┆ ---          │
        │ str                                                ┆ bool         │
        ╞════════════════════════════════════════════════════╪══════════════╡
        │ Everybody wants to rule the world                  ┆ false        │
        │ Tell me what you want, what you really really want ┆ true         │
        │ Can you feel the love tonight                      ┆ true         │
        └────────────────────────────────────────────────────┴──────────────┘

        """
        patterns = parse_as_expression(patterns, str_as_lit=False, list_as_lit=False)
        return wrap_expr(
            self._pyexpr.str_contains_any(patterns, ascii_case_insensitive)
        )
