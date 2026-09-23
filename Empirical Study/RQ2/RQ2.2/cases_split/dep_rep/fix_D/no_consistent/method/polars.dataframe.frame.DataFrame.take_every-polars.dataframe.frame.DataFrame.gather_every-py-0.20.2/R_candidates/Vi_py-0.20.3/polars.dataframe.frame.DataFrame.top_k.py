    def top_k(
        self,
        k: int,
        *,
        by: IntoExpr | Iterable[IntoExpr],
        descending: bool | Sequence[bool] = False,
        nulls_last: bool = False,
        maintain_order: bool = False,
    ) -> DataFrame:
        """
        Return the `k` largest elements.

        If 'descending=True` the smallest elements will be given.

        Parameters
        ----------
        k
            Number of rows to return.
        by
            Column(s) included in sort order. Accepts expression input.
            Strings are parsed as column names.
        descending
            Return the 'k' smallest. Top-k by multiple columns can be specified
            per column by passing a sequence of booleans.
        nulls_last
            Place null values last.
        maintain_order
            Whether the order should be maintained if elements are equal.
            Note that if `true` streaming is not possible and performance might be
            worse since this requires a stable search.

        See Also
        --------
        bottom_k

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "a": ["a", "b", "a", "b", "b", "c"],
        ...         "b": [2, 1, 1, 3, 2, 1],
        ...     }
        ... )

        Get the rows which contain the 4 largest values in column b.

        >>> df.top_k(4, by="b")
        shape: (4, 2)
        ┌─────┬─────┐
        │ a   ┆ b   │
        │ --- ┆ --- │
        │ str ┆ i64 │
        ╞═════╪═════╡
        │ b   ┆ 3   │
        │ a   ┆ 2   │
        │ b   ┆ 2   │
        │ b   ┆ 1   │
        └─────┴─────┘

        Get the rows which contain the 4 largest values when sorting on column b and a.

        >>> df.top_k(4, by=["b", "a"])
        shape: (4, 2)
        ┌─────┬─────┐
        │ a   ┆ b   │
        │ --- ┆ --- │
        │ str ┆ i64 │
        ╞═════╪═════╡
        │ b   ┆ 3   │
        │ b   ┆ 2   │
        │ a   ┆ 2   │
        │ c   ┆ 1   │
        └─────┴─────┘

        """
        return (
            self.lazy()
            .top_k(
                k,
                by=by,
                descending=descending,
                nulls_last=nulls_last,
                maintain_order=maintain_order,
            )
            .collect(
                projection_pushdown=False,
                predicate_pushdown=False,
                comm_subplan_elim=False,
                slice_pushdown=True,
            )
        )
