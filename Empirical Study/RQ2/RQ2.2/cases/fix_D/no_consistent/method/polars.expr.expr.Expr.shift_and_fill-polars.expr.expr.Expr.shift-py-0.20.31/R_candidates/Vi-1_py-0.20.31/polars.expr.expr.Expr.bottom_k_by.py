    def bottom_k_by(
        self,
        by: IntoExpr | Iterable[IntoExpr],
        k: int | IntoExprColumn = 5,
        *,
        descending: bool | Sequence[bool] = False,
        nulls_last: bool | Sequence[bool] | None = None,
        maintain_order: bool | None = None,
        multithreaded: bool | None = None,
    ) -> Self:
        r"""
        Return the elements corresponding to the `k` smallest elements of the `by` column(s).

        This has time complexity:

        .. math:: O(n + k \log{n})

        Parameters
        ----------
        by
            Column(s) used to determine the smallest elements.
            Accepts expression input. Strings are parsed as column names.
        k
            Number of elements to return.
        descending
            Consider the `k` largest elements of the `by` column(s) (instead of the `k`
            smallest). This can be specified per column by passing a sequence of
            booleans.

        nulls_last
            Place null values last.

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
        bottom_k

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "a": [1, 2, 3, 4, 5, 6],
        ...         "b": [6, 5, 4, 3, 2, 1],
        ...         "c": ["Apple", "Orange", "Apple", "Apple", "Banana", "Banana"],
        ...     }
        ... )
        >>> df
        shape: (6, 3)
        ┌─────┬─────┬────────┐
        │ a   ┆ b   ┆ c      │
        │ --- ┆ --- ┆ ---    │
        │ i64 ┆ i64 ┆ str    │
        ╞═════╪═════╪════════╡
        │ 1   ┆ 6   ┆ Apple  │
        │ 2   ┆ 5   ┆ Orange │
        │ 3   ┆ 4   ┆ Apple  │
        │ 4   ┆ 3   ┆ Apple  │
        │ 5   ┆ 2   ┆ Banana │
        │ 6   ┆ 1   ┆ Banana │
        └─────┴─────┴────────┘

        Get the bottom 2 rows by column `a` or `b`.

        >>> df.select(
        ...     pl.all().bottom_k_by("a", 2).name.suffix("_btm_by_a"),
        ...     pl.all().bottom_k_by("b", 2).name.suffix("_btm_by_b"),
        ... )
        shape: (2, 6)
        ┌────────────┬────────────┬────────────┬────────────┬────────────┬────────────┐
        │ a_btm_by_a ┆ b_btm_by_a ┆ c_btm_by_a ┆ a_btm_by_b ┆ b_btm_by_b ┆ c_btm_by_b │
        │ ---        ┆ ---        ┆ ---        ┆ ---        ┆ ---        ┆ ---        │
        │ i64        ┆ i64        ┆ str        ┆ i64        ┆ i64        ┆ str        │
        ╞════════════╪════════════╪════════════╪════════════╪════════════╪════════════╡
        │ 1          ┆ 6          ┆ Apple      ┆ 6          ┆ 1          ┆ Banana     │
        │ 2          ┆ 5          ┆ Orange     ┆ 5          ┆ 2          ┆ Banana     │
        └────────────┴────────────┴────────────┴────────────┴────────────┴────────────┘

        Get the bottom 2 rows by multiple columns with given order.

        >>> df.select(
        ...     pl.all()
        ...     .bottom_k_by(["c", "a"], 2, descending=[False, True])
        ...     .name.suffix("_by_ca"),
        ...     pl.all()
        ...     .bottom_k_by(["c", "b"], 2, descending=[False, True])
        ...     .name.suffix("_by_cb"),
        ... )
        shape: (2, 6)
        ┌─────────┬─────────┬─────────┬─────────┬─────────┬─────────┐
        │ a_by_ca ┆ b_by_ca ┆ c_by_ca ┆ a_by_cb ┆ b_by_cb ┆ c_by_cb │
        │ ---     ┆ ---     ┆ ---     ┆ ---     ┆ ---     ┆ ---     │
        │ i64     ┆ i64     ┆ str     ┆ i64     ┆ i64     ┆ str     │
        ╞═════════╪═════════╪═════════╪═════════╪═════════╪═════════╡
        │ 4       ┆ 3       ┆ Apple   ┆ 1       ┆ 6       ┆ Apple   │
        │ 3       ┆ 4       ┆ Apple   ┆ 3       ┆ 4       ┆ Apple   │
        └─────────┴─────────┴─────────┴─────────┴─────────┴─────────┘

        Get the bottom 2 rows by column `a` in each group.

        >>> (
        ...     df.group_by("c", maintain_order=True)
        ...     .agg(pl.all().bottom_k_by("a", 2))
        ...     .explode(pl.all().exclude("c"))
        ... )
        shape: (5, 3)
        ┌────────┬─────┬─────┐
        │ c      ┆ a   ┆ b   │
        │ ---    ┆ --- ┆ --- │
        │ str    ┆ i64 ┆ i64 │
        ╞════════╪═════╪═════╡
        │ Apple  ┆ 1   ┆ 6   │
        │ Apple  ┆ 3   ┆ 4   │
        │ Orange ┆ 2   ┆ 5   │
        │ Banana ┆ 5   ┆ 2   │
        │ Banana ┆ 6   ┆ 1   │
        └────────┴─────┴─────┘
        """  # noqa: W505
        if nulls_last is not None:
            issue_deprecation_warning(
                "The `nulls_last` parameter for `bottom_k_by` is deprecated."
                " It will be removed in the next breaking release."
                " Null values will be considered lowest priority and will only be"
                " included if `k` is larger than the number of non-null elements.",
                version="0.20.31",
            )
        else:
            nulls_last = False

        if maintain_order is not None:
            issue_deprecation_warning(
                "The `maintain_order` parameter for `bottom_k_by` is deprecated."
                " It will be removed in the next breaking release."
                " There will be no guarantees about the order of the output.",
                version="0.20.31",
            )
        else:
            maintain_order = False

        if multithreaded is not None:
            issue_deprecation_warning(
                "The `multithreaded` parameter for `bottom_k_by` is deprecated."
                " It will be removed in the next breaking release."
                " Polars itself will determine whether to use multithreading or not.",
                version="0.20.31",
            )
        else:
            multithreaded = True

        k = parse_as_expression(k)
        by = parse_as_list_of_expressions(by)
        descending = extend_bool(descending, len(by), "descending", "by")
        nulls_last = extend_bool(nulls_last, len(by), "nulls_last", "by")
        return self._from_pyexpr(
            self._pyexpr.bottom_k_by(
                k,
                by,
                descending=descending,
                nulls_last=nulls_last,
                maintain_order=maintain_order,
                multithreaded=multithreaded,
            )
        )
