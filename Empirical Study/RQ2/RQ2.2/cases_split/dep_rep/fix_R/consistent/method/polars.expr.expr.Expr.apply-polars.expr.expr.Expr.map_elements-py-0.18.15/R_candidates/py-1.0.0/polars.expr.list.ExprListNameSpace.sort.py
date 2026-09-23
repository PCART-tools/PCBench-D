    def sort(self, *, descending: bool = False, nulls_last: bool = False) -> Expr:
        """
        Sort the lists in this column.

        Parameters
        ----------
        descending
            Sort in descending order.
        nulls_last
            Place null values last.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "a": [[3, 2, 1], [9, 1, 2]],
        ...     }
        ... )
        >>> df.with_columns(sort=pl.col("a").list.sort())
        shape: (2, 2)
        ┌───────────┬───────────┐
        │ a         ┆ sort      │
        │ ---       ┆ ---       │
        │ list[i64] ┆ list[i64] │
        ╞═══════════╪═══════════╡
        │ [3, 2, 1] ┆ [1, 2, 3] │
        │ [9, 1, 2] ┆ [1, 2, 9] │
        └───────────┴───────────┘
        >>> df.with_columns(sort=pl.col("a").list.sort(descending=True))
        shape: (2, 2)
        ┌───────────┬───────────┐
        │ a         ┆ sort      │
        │ ---       ┆ ---       │
        │ list[i64] ┆ list[i64] │
        ╞═══════════╪═══════════╡
        │ [3, 2, 1] ┆ [3, 2, 1] │
        │ [9, 1, 2] ┆ [9, 2, 1] │
        └───────────┴───────────┘
        """
        return wrap_expr(self._pyexpr.list_sort(descending, nulls_last))
