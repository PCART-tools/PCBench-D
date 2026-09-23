    def bottom_k(
        self,
        k: int,
        *,
        by: IntoExpr | Iterable[IntoExpr],
        descending: bool | Sequence[bool] = False,
        nulls_last: bool = False,
        maintain_order: bool = False,
    ) -> Self:
        """
        Return the `k` smallest elements.

        If 'descending=True` the largest elements will be given.

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
        top_k

        Examples
        --------
        >>> lf = pl.LazyFrame(
        ...     {
        ...         "a": ["a", "b", "a", "b", "b", "c"],
        ...         "b": [2, 1, 1, 3, 2, 1],
        ...     }
        ... )

        Get the rows which contain the 4 smallest values in column b.

        >>> lf.bottom_k(4, by="b").collect()
        shape: (4, 2)
        ┌─────┬─────┐
        │ a   ┆ b   │
        │ --- ┆ --- │
        │ str ┆ i64 │
        ╞═════╪═════╡
        │ b   ┆ 1   │
        │ a   ┆ 1   │
        │ c   ┆ 1   │
        │ a   ┆ 2   │
        └─────┴─────┘

        Get the rows which contain the 4 smallest values when sorting on column a and b.

        >>> lf.bottom_k(4, by=["a", "b"]).collect()
        shape: (4, 2)
        ┌─────┬─────┐
        │ a   ┆ b   │
        │ --- ┆ --- │
        │ str ┆ i64 │
        ╞═════╪═════╡
        │ a   ┆ 1   │
        │ a   ┆ 2   │
        │ b   ┆ 1   │
        │ b   ┆ 2   │
        └─────┴─────┘

        """
        by = parse_as_list_of_expressions(by)
        if isinstance(descending, bool):
            descending = [descending]
        return self._from_pyldf(
            self._ldf.bottom_k(k, by, descending, nulls_last, maintain_order)
        )
