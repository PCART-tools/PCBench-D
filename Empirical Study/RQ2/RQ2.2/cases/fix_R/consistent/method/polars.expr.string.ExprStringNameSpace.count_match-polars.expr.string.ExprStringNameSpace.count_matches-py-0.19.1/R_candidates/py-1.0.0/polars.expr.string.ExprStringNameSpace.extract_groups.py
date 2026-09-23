    def extract_groups(self, pattern: str) -> Expr:
        r"""
        Extract all capture groups for the given regex pattern.

        Parameters
        ----------
        pattern
            A valid regular expression pattern containing at least one capture group,
            compatible with the `regex crate <https://docs.rs/regex/latest/regex/>`_.

        Notes
        -----
        All group names are **strings**.

        If your pattern contains unnamed groups, their numerical position is converted
        to a string.

        For example, here we access groups 2 and 3 via the names `"2"` and `"3"`::

            >>> df = pl.DataFrame({"col": ["foo bar baz"]})
            >>> (
            ...     df.with_columns(
            ...         pl.col("col").str.extract_groups(r"(\S+) (\S+) (.+)")
            ...     ).select(pl.col("col").struct["2"], pl.col("col").struct["3"])
            ... )
            shape: (1, 2)
            ┌─────┬─────┐
            │ 2   ┆ 3   │
            │ --- ┆ --- │
            │ str ┆ str │
            ╞═════╪═════╡
            │ bar ┆ baz │
            └─────┴─────┘

        Returns
        -------
        Expr
            Expression of data type :class:`Struct` with fields of data type
            :class:`String`.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     data={
        ...         "url": [
        ...             "http://vote.com/ballon_dor?candidate=messi&ref=python",
        ...             "http://vote.com/ballon_dor?candidate=weghorst&ref=polars",
        ...             "http://vote.com/ballon_dor?error=404&ref=rust",
        ...         ]
        ...     }
        ... )
        >>> pattern = r"candidate=(?<candidate>\w+)&ref=(?<ref>\w+)"
        >>> df.select(captures=pl.col("url").str.extract_groups(pattern)).unnest(
        ...     "captures"
        ... )
        shape: (3, 2)
        ┌───────────┬────────┐
        │ candidate ┆ ref    │
        │ ---       ┆ ---    │
        │ str       ┆ str    │
        ╞═══════════╪════════╡
        │ messi     ┆ python │
        │ weghorst  ┆ polars │
        │ null      ┆ null   │
        └───────────┴────────┘

        Unnamed groups have their numerical position converted to a string:

        >>> pattern = r"candidate=(\w+)&ref=(\w+)"
        >>> (
        ...     df.with_columns(
        ...         captures=pl.col("url").str.extract_groups(pattern)
        ...     ).with_columns(name=pl.col("captures").struct["1"].str.to_uppercase())
        ... )
        shape: (3, 3)
        ┌─────────────────────────────────┬───────────────────────┬──────────┐
        │ url                             ┆ captures              ┆ name     │
        │ ---                             ┆ ---                   ┆ ---      │
        │ str                             ┆ struct[2]             ┆ str      │
        ╞═════════════════════════════════╪═══════════════════════╪══════════╡
        │ http://vote.com/ballon_dor?can… ┆ {"messi","python"}    ┆ MESSI    │
        │ http://vote.com/ballon_dor?can… ┆ {"weghorst","polars"} ┆ WEGHORST │
        │ http://vote.com/ballon_dor?err… ┆ {null,null}           ┆ null     │
        └─────────────────────────────────┴───────────────────────┴──────────┘
        """
        return wrap_expr(self._pyexpr.str_extract_groups(pattern))
