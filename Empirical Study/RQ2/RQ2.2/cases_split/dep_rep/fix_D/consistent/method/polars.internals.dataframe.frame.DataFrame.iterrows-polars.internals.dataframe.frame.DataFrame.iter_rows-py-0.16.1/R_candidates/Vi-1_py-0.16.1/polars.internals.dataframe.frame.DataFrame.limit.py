    def limit(self: DF, n: int = 5) -> DF:
        """
        Get the first `n` rows.

        Alias for :func:`DataFrame.head`.

        Parameters
        ----------
        n
            Number of rows to return.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {"foo": [1, 2, 3, 4, 5, 6], "bar": ["a", "b", "c", "d", "e", "f"]}
        ... )
        >>> df.limit(4)
        shape: (4, 2)
        ┌─────┬─────┐
        │ foo ┆ bar │
        │ --- ┆ --- │
        │ i64 ┆ str │
        ╞═════╪═════╡
        │ 1   ┆ a   │
        │ 2   ┆ b   │
        │ 3   ┆ c   │
        │ 4   ┆ d   │
        └─────┴─────┘

        """
        return self.head(n)
