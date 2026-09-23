    def gather_every(self, n: int) -> Self:
        """
        Take every nth row in the LazyFrame and return as a new LazyFrame.

        Parameters
        ----------
        n
            Gather every *n*-th row.

        Examples
        --------
        >>> lf = pl.LazyFrame(
        ...     {
        ...         "a": [1, 2, 3, 4],
        ...         "b": [5, 6, 7, 8],
        ...     }
        ... )
        >>> lf.gather_every(2).collect()
        shape: (2, 2)
        ┌─────┬─────┐
        │ a   ┆ b   │
        │ --- ┆ --- │
        │ i64 ┆ i64 │
        ╞═════╪═════╡
        │ 1   ┆ 5   │
        │ 3   ┆ 7   │
        └─────┴─────┘
        """
        return self.select(F.col("*").gather_every(n))
