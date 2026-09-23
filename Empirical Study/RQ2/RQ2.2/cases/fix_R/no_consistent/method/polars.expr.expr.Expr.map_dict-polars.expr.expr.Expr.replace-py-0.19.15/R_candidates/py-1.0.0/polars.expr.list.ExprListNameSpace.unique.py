    def unique(self, *, maintain_order: bool = False) -> Expr:
        """
        Get the unique/distinct values in the list.

        Parameters
        ----------
        maintain_order
            Maintain order of data. This requires more work.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "a": [[1, 1, 2]],
        ...     }
        ... )
        >>> df.with_columns(unique=pl.col("a").list.unique())
        shape: (1, 2)
        ┌───────────┬───────────┐
        │ a         ┆ unique    │
        │ ---       ┆ ---       │
        │ list[i64] ┆ list[i64] │
        ╞═══════════╪═══════════╡
        │ [1, 1, 2] ┆ [1, 2]    │
        └───────────┴───────────┘
        """
        return wrap_expr(self._pyexpr.list_unique(maintain_order))
