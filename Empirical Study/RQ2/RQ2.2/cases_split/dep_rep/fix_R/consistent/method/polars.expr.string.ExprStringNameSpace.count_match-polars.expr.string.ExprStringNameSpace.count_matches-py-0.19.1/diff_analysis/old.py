    def count_match(self, pattern: str) -> Expr:
        r"""
        Count all successive non-overlapping regex matches.

        Parameters
        ----------
        pattern
            A valid regular expression pattern, compatible with the `regex crate
            <https://docs.rs/regex/latest/regex/>`_.

        Returns
        -------
        Expr
            Expression of data type :class:`UInt32`. Contains null values if the
            original value is null or the regex captures nothing.

        Examples
        --------
        >>> df = pl.DataFrame({"foo": ["123 bla 45 asd", "xyz 678 910t"]})
        >>> df.select(
        ...     pl.col("foo").str.count_match(r"\d").alias("count_digits"),
        ... )
        shape: (2, 1)
        ┌──────────────┐
        │ count_digits │
        │ ---          │
        │ u32          │
        ╞══════════════╡
        │ 5            │
        │ 6            │
        └──────────────┘

        """
        return wrap_expr(self._pyexpr.str_count_match(pattern))
