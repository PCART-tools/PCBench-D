    def set_intersection(self, other: IntoExpr) -> Expr:
        """
        Compute the SET INTERSECTION between the elements in this list and the elements of `other`.

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
        >>> df.with_columns(intersection=pl.col("a").list.set_intersection("b"))
        shape: (4, 3)
        ┌───────────┬──────────────┬──────────────┐
        │ a         ┆ b            ┆ intersection │
        │ ---       ┆ ---          ┆ ---          │
        │ list[i64] ┆ list[i64]    ┆ list[i64]    │
        ╞═══════════╪══════════════╪══════════════╡
        │ [1, 2, 3] ┆ [2, 3, 4]    ┆ [2, 3]       │
        │ []        ┆ [3]          ┆ []           │
        │ [null, 3] ┆ [3, 4, null] ┆ [null, 3]    │
        │ [5, 6, 7] ┆ [6, 8]       ┆ [6]          │
        └───────────┴──────────────┴──────────────┘
        """  # noqa: W505.
        other = parse_as_expression(other, str_as_lit=False)
        return wrap_expr(self._pyexpr.list_set_operation(other, "intersection"))
