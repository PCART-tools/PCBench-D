    def gather_every(self, n: int) -> DataFrame:
        """
        Take every nth row in the DataFrame and return as a new DataFrame.

        Parameters
        ----------
        n
            Gather every *n*-th row.

        Examples
        --------
        >>> s = pl.DataFrame({"a": [1, 2, 3, 4], "b": [5, 6, 7, 8]})
        >>> s.gather_every(2)
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
