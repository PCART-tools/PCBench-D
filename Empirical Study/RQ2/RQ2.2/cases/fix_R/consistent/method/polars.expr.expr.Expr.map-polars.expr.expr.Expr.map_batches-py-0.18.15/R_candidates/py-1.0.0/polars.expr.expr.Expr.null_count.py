    def null_count(self) -> Expr:
        """
        Count null values.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "a": [None, 1, None],
        ...         "b": [10, None, 300],
        ...         "c": [350, 650, 850],
        ...     }
        ... )
        >>> df.select(pl.all().null_count())
        shape: (1, 3)
        ┌─────┬─────┬─────┐
        │ a   ┆ b   ┆ c   │
        │ --- ┆ --- ┆ --- │
        │ u32 ┆ u32 ┆ u32 │
        ╞═════╪═════╪═════╡
        │ 2   ┆ 1   ┆ 0   │
        └─────┴─────┴─────┘
        """
        return self._from_pyexpr(self._pyexpr.null_count())
