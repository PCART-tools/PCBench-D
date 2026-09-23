    def head(self, n: int = 5) -> LazyFrame:
        """
        Get the first `n` rows.

        Parameters
        ----------
        n
            Number of rows to return.

        Notes
        -----
        Consider using the :func:`fetch` operation if you only want to test your
        query. The :func:`fetch` operation will load the first `n` rows at the scan
        level, whereas the :func:`head`/:func:`limit` are applied at the end.

        Examples
        --------
        >>> lf = pl.LazyFrame(
        ...     {
        ...         "a": [1, 2, 3, 4, 5, 6],
        ...         "b": [7, 8, 9, 10, 11, 12],
        ...     }
        ... )
        >>> lf.head().collect()
        shape: (5, 2)
        ┌─────┬─────┐
        │ a   ┆ b   │
        │ --- ┆ --- │
        │ i64 ┆ i64 │
        ╞═════╪═════╡
        │ 1   ┆ 7   │
        │ 2   ┆ 8   │
        │ 3   ┆ 9   │
        │ 4   ┆ 10  │
        │ 5   ┆ 11  │
        └─────┴─────┘
        >>> lf.head(2).collect()
        shape: (2, 2)
        ┌─────┬─────┐
        │ a   ┆ b   │
        │ --- ┆ --- │
        │ i64 ┆ i64 │
        ╞═════╪═════╡
        │ 1   ┆ 7   │
        │ 2   ┆ 8   │
        └─────┴─────┘
        """
        return self.slice(0, n)
