    def set_difference(self, other: IntoExpr) -> Expr:
        """
        Compute the SET DIFFERENCE between the elements in this list and the elements of ``other``.

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
        >>> df.with_columns(pl.col("a").list.set_difference("b").alias("difference"))
        shape: (4, 3)
        ┌───────────┬──────────────┬────────────┐
        │ a         ┆ b            ┆ difference │
        │ ---       ┆ ---          ┆ ---        │
        │ list[i64] ┆ list[i64]    ┆ list[i64]  │
        ╞═══════════╪══════════════╪════════════╡
        │ [1, 2, 3] ┆ [2, 3, 4]    ┆ [1]        │
        │ []        ┆ [3]          ┆ []         │
        │ [null, 3] ┆ [3, 4, null] ┆ []         │
        │ [5, 6, 7] ┆ [6, 8]       ┆ [5, 7]     │
        └───────────┴──────────────┴────────────┘

        See Also
        --------
        polars.Expr.list.diff: Calculates the n-th discrete difference of every sublist.

        """  # noqa: W505.
        other = parse_as_expression(other, str_as_lit=False)
        return wrap_expr(self._pyexpr.list_set_operation(other, "difference"))
