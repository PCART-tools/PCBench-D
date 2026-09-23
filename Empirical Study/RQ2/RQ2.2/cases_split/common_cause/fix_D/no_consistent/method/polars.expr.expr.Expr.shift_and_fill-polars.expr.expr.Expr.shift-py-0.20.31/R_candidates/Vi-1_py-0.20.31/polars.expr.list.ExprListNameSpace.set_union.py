    def set_union(self, other: IntoExpr) -> Expr:
        """
        Compute the SET UNION between the elements in this list and the elements of `other`.

        Parameters
        ----------
        other
            Right hand side of the set operation.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "a": [[1, 2, 3], [], [None, 3], [5, 6, 7]],
        ...         "b": [[2, 3, 4], [3], [3, 4, None], [6, 8]],
        ...     }
        ... )
        >>> df.with_columns(
        ...     union=pl.col("a").list.set_union("b")
        ... )  # doctest: +IGNORE_RESULT
        shape: (4, 3)
        ┌───────────┬──────────────┬───────────────┐
        │ a         ┆ b            ┆ union         │
        │ ---       ┆ ---          ┆ ---           │
        │ list[i64] ┆ list[i64]    ┆ list[i64]     │
        ╞═══════════╪══════════════╪═══════════════╡
        │ [1, 2, 3] ┆ [2, 3, 4]    ┆ [1, 2, 3, 4]  │
        │ []        ┆ [3]          ┆ [3]           │
        │ [null, 3] ┆ [3, 4, null] ┆ [null, 3, 4]  │
        │ [5, 6, 7] ┆ [6, 8]       ┆ [5, 6, 7, 8]  │
        └───────────┴──────────────┴───────────────┘
        """  # noqa: W505.
        other = parse_as_expression(other, str_as_lit=False)
        return wrap_expr(self._pyexpr.list_set_operation(other, "union"))
