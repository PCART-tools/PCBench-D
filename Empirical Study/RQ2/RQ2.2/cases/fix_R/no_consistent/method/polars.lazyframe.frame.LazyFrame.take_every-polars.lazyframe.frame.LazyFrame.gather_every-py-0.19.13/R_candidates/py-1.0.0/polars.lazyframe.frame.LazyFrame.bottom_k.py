    @deprecate_renamed_parameter("descending", "reverse", version="1.0.0")
    def bottom_k(
        self,
        k: int,
        *,
        by: IntoExpr | Iterable[IntoExpr],
        reverse: bool | Sequence[bool] = False,
    ) -> LazyFrame:
        """
        Return the `k` smallest rows.

        Non-null elements are always preferred over null elements, regardless of
        the value of `reverse`. The output is not guaranteed to be in any
        particular order, call :func:`sort` after this function if you wish the
        output to be sorted.

        Parameters
        ----------
        k
            Number of rows to return.
        by
            Column(s) used to determine the bottom rows.
            Accepts expression input. Strings are parsed as column names.
        reverse
            Consider the `k` largest elements of the `by` column(s) (instead of the `k`
            smallest). This can be specified per column by passing a sequence of
            booleans.

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
        by = parse_into_list_of_expressions(by)
        reverse = extend_bool(reverse, len(by), "reverse", "by")
        return self._from_pyldf(self._ldf.bottom_k(k, by=by, reverse=reverse))
