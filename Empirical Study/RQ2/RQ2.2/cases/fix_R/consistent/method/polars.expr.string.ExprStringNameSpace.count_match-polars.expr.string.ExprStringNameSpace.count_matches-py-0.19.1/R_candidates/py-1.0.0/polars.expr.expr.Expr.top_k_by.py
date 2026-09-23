    @deprecate_renamed_parameter("descending", "reverse", version="1.0.0")
    def top_k_by(
        self,
        by: IntoExpr | Iterable[IntoExpr],
        k: int | IntoExprColumn = 5,
        *,
        reverse: bool | Sequence[bool] = False,
    ) -> Expr:
        r"""
        Return the elements corresponding to the `k` largest elements of the `by` column(s).

        Non-null elements are always preferred over null elements, regardless of
        the value of `reverse`. The output is not guaranteed to be in any
        particular order, call :func:`sort` after this function if you wish the
        output to be sorted.

        This has time complexity:

        .. math:: O(n \log{n})

        Parameters
        ----------
        by
            Column(s) used to determine the largest elements.
            Accepts expression input. Strings are parsed as column names.
        k
            Number of elements to return.
        reverse
            Consider the `k` smallest elements of the `by` column(s) (instead of the `k`
            largest). This can be specified per column by passing a sequence of
            booleans.

        See Also
        --------
        top_k
        bottom_k
        bottom_k_by

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

        Get the top 2 rows by column `a` or `b`.

        >>> df.select(
        ...     pl.all().top_k_by("a", 2).name.suffix("_top_by_a"),
        ...     pl.all().top_k_by("b", 2).name.suffix("_top_by_b"),
        ... )
        shape: (2, 6)
        ┌────────────┬────────────┬────────────┬────────────┬────────────┬────────────┐
        │ a_top_by_a ┆ b_top_by_a ┆ c_top_by_a ┆ a_top_by_b ┆ b_top_by_b ┆ c_top_by_b │
        │ ---        ┆ ---        ┆ ---        ┆ ---        ┆ ---        ┆ ---        │
        │ i64        ┆ i64        ┆ str        ┆ i64        ┆ i64        ┆ str        │
        ╞════════════╪════════════╪════════════╪════════════╪════════════╪════════════╡
        │ 6          ┆ 1          ┆ Banana     ┆ 1          ┆ 6          ┆ Apple      │
        │ 5          ┆ 2          ┆ Banana     ┆ 2          ┆ 5          ┆ Orange     │
        └────────────┴────────────┴────────────┴────────────┴────────────┴────────────┘

        Get the top 2 rows by multiple columns with given order.

        >>> df.select(
        ...     pl.all()
        ...     .top_k_by(["c", "a"], 2, reverse=[False, True])
        ...     .name.suffix("_by_ca"),
        ...     pl.all()
        ...     .top_k_by(["c", "b"], 2, reverse=[False, True])
        ...     .name.suffix("_by_cb"),
        ... )
        shape: (2, 6)
        ┌─────────┬─────────┬─────────┬─────────┬─────────┬─────────┐
        │ a_by_ca ┆ b_by_ca ┆ c_by_ca ┆ a_by_cb ┆ b_by_cb ┆ c_by_cb │
        │ ---     ┆ ---     ┆ ---     ┆ ---     ┆ ---     ┆ ---     │
        │ i64     ┆ i64     ┆ str     ┆ i64     ┆ i64     ┆ str     │
        ╞═════════╪═════════╪═════════╪═════════╪═════════╪═════════╡
        │ 2       ┆ 5       ┆ Orange  ┆ 2       ┆ 5       ┆ Orange  │
        │ 5       ┆ 2       ┆ Banana  ┆ 6       ┆ 1       ┆ Banana  │
        └─────────┴─────────┴─────────┴─────────┴─────────┴─────────┘

        Get the top 2 rows by column `a` in each group.

        >>> (
        ...     df.group_by("c", maintain_order=True)
        ...     .agg(pl.all().top_k_by("a", 2))
        ...     .explode(pl.all().exclude("c"))
        ... )
        shape: (5, 3)
        ┌────────┬─────┬─────┐
        │ c      ┆ a   ┆ b   │
        │ ---    ┆ --- ┆ --- │
        │ str    ┆ i64 ┆ i64 │
        ╞════════╪═════╪═════╡
        │ Apple  ┆ 4   ┆ 3   │
        │ Apple  ┆ 3   ┆ 4   │
        │ Orange ┆ 2   ┆ 5   │
        │ Banana ┆ 6   ┆ 1   │
        │ Banana ┆ 5   ┆ 2   │
        └────────┴─────┴─────┘
        """  # noqa: W505
        k = parse_into_expression(k)
        by = parse_into_list_of_expressions(by)
        reverse = extend_bool(reverse, len(by), "reverse", "by")
        return self._from_pyexpr(self._pyexpr.top_k_by(by, k=k, reverse=reverse))
