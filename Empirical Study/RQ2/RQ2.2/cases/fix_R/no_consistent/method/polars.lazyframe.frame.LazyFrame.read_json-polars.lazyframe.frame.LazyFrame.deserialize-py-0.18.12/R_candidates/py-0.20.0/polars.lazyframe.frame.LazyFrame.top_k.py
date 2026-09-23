    def top_k(
        self,
        k: int,
        *,
        by: IntoExpr | Iterable[IntoExpr],
        descending: bool | Sequence[bool] = False,
        nulls_last: bool = False,
        maintain_order: bool = False,
    ) -> Self:
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
            Note that if `true` streaming is not possible and performance might
            be worse since this requires a stable search.

        See Also
        --------
        bottom_k

        Examples
        --------
        >>> lf = pl.LazyFrame(
        ...     {
        ...         "a": ["a", "b", "a", "b", "b", "c"],
        ...         "b": [2, 1, 1, 3, 2, 1],
        ...     }
        ... )

        Get the rows which contain the 4 largest values in column b.

        >>> lf.top_k(4, by="b").collect()
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

        >>> lf.top_k(4, by=["b", "a"]).collect()
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
        by = parse_as_list_of_expressions(by)
        if isinstance(descending, bool):
            descending = [descending]
        elif len(by) != len(descending):
            raise ValueError(
                f"the length of `descending` ({len(descending)}) does not match the length of `by` ({len(by)})"
            )
        return self._from_pyldf(
            self._ldf.top_k(k, by, descending, nulls_last, maintain_order)
        )
