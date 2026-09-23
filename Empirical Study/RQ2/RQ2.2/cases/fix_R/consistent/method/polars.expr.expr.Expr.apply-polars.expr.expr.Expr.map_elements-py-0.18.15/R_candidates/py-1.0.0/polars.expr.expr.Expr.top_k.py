    def top_k(self, k: int | IntoExprColumn = 5) -> Expr:
        r"""
        Return the `k` largest elements.

        Non-null elements are always preferred over null elements. The output
        is not guaranteed to be in any particular order, call :func:`sort`
        after this function if you wish the output to be sorted.

        This has time complexity:

        .. math:: O(n)

        Parameters
        ----------
        k
            Number of elements to return.

        See Also
        --------
        top_k_by
        bottom_k
        bottom_k_by

        Examples
        --------
        Get the 5 largest values in series.

        >>> df = pl.DataFrame({"value": [1, 98, 2, 3, 99, 4]})
        >>> df.select(
        ...     pl.col("value").top_k().alias("top_k"),
        ...     pl.col("value").bottom_k().alias("bottom_k"),
        ... )
        shape: (5, 2)
        ┌───────┬──────────┐
        │ top_k ┆ bottom_k │
        │ ---   ┆ ---      │
        │ i64   ┆ i64      │
        ╞═══════╪══════════╡
        │ 4     ┆ 1        │
        │ 98    ┆ 98       │
        │ 2     ┆ 2        │
        │ 3     ┆ 3        │
        │ 99    ┆ 4        │
        └───────┴──────────┘
        """
        k = parse_into_expression(k)
        return self._from_pyexpr(self._pyexpr.top_k(k))
