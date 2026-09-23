    def splitn(self, by: IntoExpr, n: int) -> Expr:
        """
        Split the string by a substring, restricted to returning at most ``n`` items.

        If the number of possible splits is less than ``n-1``, the remaining field
        elements will be null. If the number of possible splits is ``n-1`` or greater,
        the last (nth) substring will contain the remainder of the string.

        Parameters
        ----------
        by
            Substring to split by.
        n
            Max number of items to return.

        Returns
        -------
        Expr
            Expression of data type :class:`Struct` with fields of data type
            :class:`Utf8`.

        Examples
        --------
        >>> df = pl.DataFrame({"s": ["foo bar", None, "foo-bar", "foo bar baz"]})
        >>> df.select(pl.col("s").str.splitn(" ", 2).alias("fields"))
        shape: (4, 1)
        ┌───────────────────┐
        │ fields            │
        │ ---               │
        │ struct[2]         │
        ╞═══════════════════╡
        │ {"foo","bar"}     │
        │ {null,null}       │
        │ {"foo-bar",null}  │
        │ {"foo","bar baz"} │
        └───────────────────┘

        Split string values in column s in exactly 2 parts and assign
        each part to a new column.

        >>> df.with_columns(
        ...     [
        ...         pl.col("s")
        ...         .str.splitn(" ", 2)
        ...         .struct.rename_fields(["first_part", "second_part"])
        ...         .alias("fields"),
        ...     ]
        ... ).unnest("fields")
        shape: (4, 3)
        ┌─────────────┬────────────┬─────────────┐
        │ s           ┆ first_part ┆ second_part │
        │ ---         ┆ ---        ┆ ---         │
        │ str         ┆ str        ┆ str         │
        ╞═════════════╪════════════╪═════════════╡
        │ foo bar     ┆ foo        ┆ bar         │
        │ null        ┆ null       ┆ null        │
        │ foo-bar     ┆ foo-bar    ┆ null        │
        │ foo bar baz ┆ foo        ┆ bar baz     │
        └─────────────┴────────────┴─────────────┘

        """
        by = parse_as_expression(by, str_as_lit=True)
        return wrap_expr(self._pyexpr.str_splitn(by, n))
