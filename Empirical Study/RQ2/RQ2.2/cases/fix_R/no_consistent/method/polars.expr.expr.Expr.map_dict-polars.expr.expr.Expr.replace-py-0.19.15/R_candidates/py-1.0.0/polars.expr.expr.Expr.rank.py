    def rank(
        self,
        method: RankMethod = "average",
        *,
        descending: bool = False,
        seed: int | None = None,
    ) -> Expr:
        """
        Assign ranks to data, dealing with ties appropriately.

        Parameters
        ----------
        method : {'average', 'min', 'max', 'dense', 'ordinal', 'random'}
            The method used to assign ranks to tied elements.
            The following methods are available (default is 'average'):

            - 'average' : The average of the ranks that would have been assigned to
              all the tied values is assigned to each value.
            - 'min' : The minimum of the ranks that would have been assigned to all
              the tied values is assigned to each value. (This is also referred to
              as "competition" ranking.)
            - 'max' : The maximum of the ranks that would have been assigned to all
              the tied values is assigned to each value.
            - 'dense' : Like 'min', but the rank of the next highest element is
              assigned the rank immediately after those assigned to the tied
              elements.
            - 'ordinal' : All values are given a distinct rank, corresponding to
              the order that the values occur in the Series.
            - 'random' : Like 'ordinal', but the rank for ties is not dependent
              on the order that the values occur in the Series.
        descending
            Rank in descending order.
        seed
            If `method="random"`, use this as seed.

        Examples
        --------
        The 'average' method:

        >>> df = pl.DataFrame({"a": [3, 6, 1, 1, 6]})
        >>> df.select(pl.col("a").rank())
        shape: (5, 1)
        ┌─────┐
        │ a   │
        │ --- │
        │ f64 │
        ╞═════╡
        │ 3.0 │
        │ 4.5 │
        │ 1.5 │
        │ 1.5 │
        │ 4.5 │
        └─────┘

        The 'ordinal' method:

        >>> df = pl.DataFrame({"a": [3, 6, 1, 1, 6]})
        >>> df.select(pl.col("a").rank("ordinal"))
        shape: (5, 1)
        ┌─────┐
        │ a   │
        │ --- │
        │ u32 │
        ╞═════╡
        │ 3   │
        │ 4   │
        │ 1   │
        │ 2   │
        │ 5   │
        └─────┘

        Use 'rank' with 'over' to rank within groups:

        >>> df = pl.DataFrame({"a": [1, 1, 2, 2, 2], "b": [6, 7, 5, 14, 11]})
        >>> df.with_columns(pl.col("b").rank().over("a").alias("rank"))
        shape: (5, 3)
        ┌─────┬─────┬──────┐
        │ a   ┆ b   ┆ rank │
        │ --- ┆ --- ┆ ---  │
        │ i64 ┆ i64 ┆ f64  │
        ╞═════╪═════╪══════╡
        │ 1   ┆ 6   ┆ 1.0  │
        │ 1   ┆ 7   ┆ 2.0  │
        │ 2   ┆ 5   ┆ 1.0  │
        │ 2   ┆ 14  ┆ 3.0  │
        │ 2   ┆ 11  ┆ 2.0  │
        └─────┴─────┴──────┘
        """
        return self._from_pyexpr(self._pyexpr.rank(method, descending, seed))
