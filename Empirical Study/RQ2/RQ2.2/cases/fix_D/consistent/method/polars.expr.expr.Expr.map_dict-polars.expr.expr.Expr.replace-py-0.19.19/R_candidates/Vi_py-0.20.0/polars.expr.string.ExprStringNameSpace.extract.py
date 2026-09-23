    def extract(self, pattern: str, group_index: int = 1) -> Expr:
        r"""
        Extract the target capture group from provided patterns.

        Parameters
        ----------
        pattern
            A valid regular expression pattern, compatible with the `regex crate
            <https://docs.rs/regex/latest/regex/>`_.
        group_index
            Index of the targeted capture group.
            Group 0 means the whole pattern, the first group begins at index 1.
            Defaults to the first capture group.

        Notes
        -----
        To modify regular expression behaviour (such as multi-line matching)
        with flags, use the inline `(?iLmsuxU)` syntax. For example:

        >>> df = pl.DataFrame(
        ...     data={
        ...         "lines": [
        ...             "I Like\nThose\nOdds",
        ...             "This is\nThe Way",
        ...         ]
        ...     }
        ... )
        >>> df.with_columns(
        ...     pl.col("lines").str.extract(r"(?m)^(T\w+)", 1).alias("matches"),
        ... )
        shape: (2, 2)
        ┌─────────┬─────────┐
        │ lines   ┆ matches │
        │ ---     ┆ ---     │
        │ str     ┆ str     │
        ╞═════════╪═════════╡
        │ I Like  ┆ Those   │
        │ Those   ┆         │
        │ Odds    ┆         │
        │ This is ┆ This    │
        │ The Way ┆         │
        └─────────┴─────────┘

        See the regex crate's section on `grouping and flags
        <https://docs.rs/regex/latest/regex/#grouping-and-flags>`_ for
        additional information about the use of inline expression modifiers.

        Returns
        -------
        Expr
            Expression of data type :class:`Utf8`. Contains null values if original
            value is null or the regex captures nothing.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "url": [
        ...             "http://vote.com/ballon_dor?error=404&ref=unknown",
        ...             "http://vote.com/ballon_dor?ref=polars&candidate=messi",
        ...             "http://vote.com/ballon_dor?candidate=ronaldo&ref=polars",
        ...         ]
        ...     }
        ... )
        >>> df.select(
        ...     pl.col("url").str.extract(r"candidate=(\w+)", 1).alias("candidate"),
        ...     pl.col("url").str.extract(r"ref=(\w+)", 1).alias("referer"),
        ...     pl.col("url").str.extract(r"error=(\w+)", 1).alias("error"),
        ... )
        shape: (3, 3)
        ┌───────────┬─────────┬───────┐
        │ candidate ┆ referer ┆ error │
        │ ---       ┆ ---     ┆ ---   │
        │ str       ┆ str     ┆ str   │
        ╞═══════════╪═════════╪═══════╡
        │ null      ┆ unknown ┆ 404   │
        │ messi     ┆ polars  ┆ null  │
        │ ronaldo   ┆ polars  ┆ null  │
        └───────────┴─────────┴───────┘

        """
        return wrap_expr(self._pyexpr.str_extract(pattern, group_index))
