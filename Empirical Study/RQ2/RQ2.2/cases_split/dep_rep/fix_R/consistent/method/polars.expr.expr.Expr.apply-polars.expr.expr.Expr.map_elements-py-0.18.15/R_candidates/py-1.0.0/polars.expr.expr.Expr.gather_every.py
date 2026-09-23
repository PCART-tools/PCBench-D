    def gather_every(self, n: int, offset: int = 0) -> Expr:
        """
        Take every nth value in the Series and return as a new Series.

        Parameters
        ----------
        n
            Gather every *n*-th row.
        offset
            Starting index.

        Examples
        --------
        >>> df = pl.DataFrame({"foo": [1, 2, 3, 4, 5, 6, 7, 8, 9]})
        >>> df.select(pl.col("foo").gather_every(3))
        shape: (3, 1)
        ┌─────┐
        │ foo │
        │ --- │
        │ i64 │
        ╞═════╡
        │ 1   │
        │ 4   │
        │ 7   │
        └─────┘

        >>> df.select(pl.col("foo").gather_every(3, offset=1))
        shape: (3, 1)
        ┌─────┐
        │ foo │
        │ --- │
        │ i64 │
        ╞═════╡
        │ 2   │
        │ 5   │
        │ 8   │
        └─────┘
        """
        return self._from_pyexpr(self._pyexpr.gather_every(n, offset))
