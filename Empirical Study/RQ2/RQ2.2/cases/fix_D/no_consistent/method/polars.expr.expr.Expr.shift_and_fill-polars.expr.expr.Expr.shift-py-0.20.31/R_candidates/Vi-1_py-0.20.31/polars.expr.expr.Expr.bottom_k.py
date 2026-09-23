    def bottom_k(
        self,
        k: int | IntoExprColumn = 5,
        *,
        nulls_last: bool | None = None,
        maintain_order: bool | None = None,
        multithreaded: bool | None = None,
    ) -> Self:
        r"""
        Return the `k` smallest elements.

        This has time complexity:

        .. math:: O(n + k \log{n})

        Parameters
        ----------
        k
            Number of elements to return.

        nulls_last
            Place null values last.

            .. deprecated:: 0.20.31
                This parameter will be removed in the next breaking release.
                Null values will be considered lowest priority and will only be
                included if `k` is larger than the number of non-null elements.

        maintain_order
            Whether the order should be maintained if elements are equal.

            .. deprecated:: 0.20.31
                This parameter will be removed in the next breaking release.
                There will be no guarantees about the order of the output.

        multithreaded
            Sort using multiple threads.

            .. deprecated:: 0.20.31
                This parameter will be removed in the next breaking release.
                Polars itself will determine whether to use multithreading or not.

        See Also
        --------
        top_k
        top_k_by
        bottom_k_by

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "value": [1, 98, 2, 3, 99, 4],
        ...     }
        ... )
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
        │ 99    ┆ 1        │
        │ 98    ┆ 2        │
        │ 4     ┆ 3        │
        │ 3     ┆ 4        │
        │ 2     ┆ 98       │
        └───────┴──────────┘
        """
        if nulls_last is not None:
            issue_deprecation_warning(
                "The `nulls_last` parameter for `bottom_k` is deprecated."
                " It will be removed in the next breaking release."
                " Null values will be considered lowest priority and will only be"
                " included if `k` is larger than the number of non-null elements.",
                version="0.20.31",
            )
        else:
            nulls_last = False

        if maintain_order is not None:
            issue_deprecation_warning(
                "The `maintain_order` parameter for `bottom_k` is deprecated."
                " It will be removed in the next breaking release."
                " There will be no guarantees about the order of the output.",
                version="0.20.31",
            )
        else:
            maintain_order = False

        if multithreaded is not None:
            issue_deprecation_warning(
                "The `multithreaded` parameter for `bottom_k` is deprecated."
                " It will be removed in the next breaking release."
                " Polars itself will determine whether to use multithreading or not.",
                version="0.20.31",
            )
        else:
            multithreaded = True

        k = parse_as_expression(k)
        return self._from_pyexpr(
            self._pyexpr.bottom_k(
                k,
                nulls_last=nulls_last,
                maintain_order=maintain_order,
                multithreaded=multithreaded,
            )
        )
