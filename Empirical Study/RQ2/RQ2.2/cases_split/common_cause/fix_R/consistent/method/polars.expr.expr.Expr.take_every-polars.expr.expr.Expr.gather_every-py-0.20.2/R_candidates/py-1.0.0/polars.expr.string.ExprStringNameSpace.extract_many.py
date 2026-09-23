    @unstable()
    def extract_many(
        self,
        patterns: IntoExpr,
        *,
        ascii_case_insensitive: bool = False,
        overlapping: bool = False,
    ) -> Expr:
        """

        Use the aho-corasick algorithm to extract many matches.

        Parameters
        ----------
        patterns
            String patterns to search.
        ascii_case_insensitive
            Enable ASCII-aware case insensitive matching.
            When this option is enabled, searching will be performed without respect
            to case for ASCII letters (a-z and A-Z) only.
        overlapping
            Whether matches may overlap.

        Examples
        --------
        >>> _ = pl.Config.set_fmt_str_lengths(100)
        >>> df = pl.DataFrame({"values": ["discontent"]})
        >>> patterns = ["winter", "disco", "onte", "discontent"]
        >>> df.with_columns(
        ...     pl.col("values")
        ...     .str.extract_many(patterns, overlapping=False)
        ...     .alias("matches"),
        ...     pl.col("values")
        ...     .str.extract_many(patterns, overlapping=True)
        ...     .alias("matches_overlapping"),
        ... )
        shape: (1, 3)
        ┌────────────┬───────────┬─────────────────────────────────┐
        │ values     ┆ matches   ┆ matches_overlapping             │
        │ ---        ┆ ---       ┆ ---                             │
        │ str        ┆ list[str] ┆ list[str]                       │
        ╞════════════╪═══════════╪═════════════════════════════════╡
        │ discontent ┆ ["disco"] ┆ ["disco", "onte", "discontent"] │
        └────────────┴───────────┴─────────────────────────────────┘
        >>> df = pl.DataFrame(
        ...     {
        ...         "values": ["discontent", "rhapsody"],
        ...         "patterns": [
        ...             ["winter", "disco", "onte", "discontent"],
        ...             ["rhap", "ody", "coalesce"],
        ...         ],
        ...     }
        ... )
        >>> df.select(pl.col("values").str.extract_many("patterns"))
        shape: (2, 1)
        ┌─────────────────┐
        │ values          │
        │ ---             │
        │ list[str]       │
        ╞═════════════════╡
        │ ["disco"]       │
        │ ["rhap", "ody"] │
        └─────────────────┘

        """
        patterns = parse_into_expression(
            patterns, str_as_lit=False, list_as_series=True
        )
        return wrap_expr(
            self._pyexpr.str_extract_many(patterns, ascii_case_insensitive, overlapping)
        )
