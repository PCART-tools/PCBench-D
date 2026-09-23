    def sort(self, *, descending: bool = False) -> Expr:
        """
        Sort the arrays in this column.

        Parameters
        ----------
        descending
            Sort in descending order.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "a": [[3, 2, 1], [9, 1, 2]],
        ...     }
        ... )
        >>> df.select(pl.col("a").list.sort())
        shape: (2, 1)
        ┌───────────┐
        │ a         │
        │ ---       │
        │ list[i64] │
        ╞═══════════╡
        │ [1, 2, 3] │
        │ [1, 2, 9] │
        └───────────┘
        >>> df.select(pl.col("a").list.sort(descending=True))
        shape: (2, 1)
        ┌───────────┐
        │ a         │
        │ ---       │
        │ list[i64] │
        ╞═══════════╡
        │ [3, 2, 1] │
        │ [9, 2, 1] │
        └───────────┘

        """
        return wrap_expr(self._pyexpr.list_sort(descending))
