    def extract_all(self, pattern: str | Expr) -> Expr:
        r'''
        Extract all matches for the given regex pattern.

        Extract each successive non-overlapping regex match in an individual string
        as a list. If the haystack string is `null`, `null` is returned.

        Parameters
        ----------
        pattern
            A valid regular expression pattern, compatible with the `regex crate
            <https://docs.rs/regex/latest/regex/>`_.

        Notes
        -----
        To modify regular expression behaviour (such as "verbose" mode and/or
        case-sensitive matching) with flags, use the inline `(?iLmsuxU)` syntax.
        For example:

        >>> df = pl.DataFrame(
        ...     data={
        ...         "email": [
        ...             "real.email@spam.com",
        ...             "some_account@somewhere.net",
        ...             "abc.def.ghi.jkl@uvw.xyz.co.uk",
        ...         ]
        ...     }
        ... )
        >>> # extract name/domain parts from the addresses, using verbose regex
        >>> df.with_columns(
        ...     pl.col("email")
        ...     .str.extract_all(
        ...         r"""(?xi)   # activate 'verbose' and 'case-insensitive' flags
        ...         [           # (start character group)
        ...           A-Z       # letters
        ...           0-9       # digits
        ...           ._%+\-    # special chars
        ...         ]           # (end character group)
        ...         +           # 'one or more' quantifier
        ...         """
        ...     )
        ...     .list.to_struct(fields=["name", "domain"])
        ...     .alias("email_parts")
        ... ).unnest("email_parts")
        shape: (3, 3)
        ┌───────────────────────────────┬─────────────────┬───────────────┐
        │ email                         ┆ name            ┆ domain        │
        │ ---                           ┆ ---             ┆ ---           │
        │ str                           ┆ str             ┆ str           │
        ╞═══════════════════════════════╪═════════════════╪═══════════════╡
        │ real.email@spam.com           ┆ real.email      ┆ spam.com      │
        │ some_account@somewhere.net    ┆ some_account    ┆ somewhere.net │
        │ abc.def.ghi.jkl@uvw.xyz.co.uk ┆ abc.def.ghi.jkl ┆ uvw.xyz.co.uk │
        └───────────────────────────────┴─────────────────┴───────────────┘

        See the regex crate's section on `grouping and flags
        <https://docs.rs/regex/latest/regex/#grouping-and-flags>`_ for
        additional information about the use of inline expression modifiers.

        Returns
        -------
        Expr
            Expression of data type `List(String)`.

        Examples
        --------
        >>> df = pl.DataFrame({"foo": ["123 bla 45 asd", "xyz 678 910t", "bar", None]})
        >>> df.select(
        ...     pl.col("foo").str.extract_all(r"\d+").alias("extracted_nrs"),
        ... )
        shape: (4, 1)
        ┌────────────────┐
        │ extracted_nrs  │
        │ ---            │
        │ list[str]      │
        ╞════════════════╡
        │ ["123", "45"]  │
        │ ["678", "910"] │
        │ []             │
        │ null           │
        └────────────────┘

        '''
        pattern = parse_as_expression(pattern, str_as_lit=True)
        return wrap_expr(self._pyexpr.str_extract_all(pattern))
