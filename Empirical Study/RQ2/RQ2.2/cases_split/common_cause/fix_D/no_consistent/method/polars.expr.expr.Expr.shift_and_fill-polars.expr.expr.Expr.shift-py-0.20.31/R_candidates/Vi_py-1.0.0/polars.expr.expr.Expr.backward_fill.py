    def backward_fill(self, limit: int | None = None) -> Expr:
        """
        Fill missing values with the next to be seen values.

        Parameters
        ----------
        limit
            The number of consecutive null values to backward fill.

        See Also
        --------
        forward_fill
        shift

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "a": [1, 2, None],
        ...         "b": [4, None, 6],
        ...         "c": [None, None, 2],
        ...     }
        ... )
        >>> df.select(pl.all().backward_fill())
        shape: (3, 3)
        ┌──────┬─────┬─────┐
        │ a    ┆ b   ┆ c   │
        │ ---  ┆ --- ┆ --- │
        │ i64  ┆ i64 ┆ i64 │
        ╞══════╪═════╪═════╡
        │ 1    ┆ 4   ┆ 2   │
        │ 2    ┆ 6   ┆ 2   │
        │ null ┆ 6   ┆ 2   │
        └──────┴─────┴─────┘
        >>> df.select(pl.all().backward_fill(limit=1))
        shape: (3, 3)
        ┌──────┬─────┬──────┐
        │ a    ┆ b   ┆ c    │
        │ ---  ┆ --- ┆ ---  │
        │ i64  ┆ i64 ┆ i64  │
        ╞══════╪═════╪══════╡
        │ 1    ┆ 4   ┆ null │
        │ 2    ┆ 6   ┆ 2    │
        │ null ┆ 6   ┆ 2    │
        └──────┴─────┴──────┘
        """
        return self._from_pyexpr(self._pyexpr.backward_fill(limit))
