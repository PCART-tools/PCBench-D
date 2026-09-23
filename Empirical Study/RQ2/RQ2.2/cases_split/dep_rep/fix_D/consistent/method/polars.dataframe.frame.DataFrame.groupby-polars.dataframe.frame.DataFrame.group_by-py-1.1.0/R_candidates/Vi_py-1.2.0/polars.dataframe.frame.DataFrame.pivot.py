    @deprecate_renamed_parameter("columns", "on", version="1.0.0")
    def pivot(
        self,
        on: ColumnNameOrSelector | Sequence[ColumnNameOrSelector],
        *,
        index: ColumnNameOrSelector | Sequence[ColumnNameOrSelector] | None = None,
        values: ColumnNameOrSelector | Sequence[ColumnNameOrSelector] | None = None,
        aggregate_function: PivotAgg | Expr | None = None,
        maintain_order: bool = True,
        sort_columns: bool = False,
        separator: str = "_",
    ) -> DataFrame:
        """
        Create a spreadsheet-style pivot table as a DataFrame.

        Only available in eager mode. See "Examples" section below for how to do a
        "lazy pivot" if you know the unique column values in advance.

        Parameters
        ----------
        on
            Name of the column(s) whose values will be used as the header of the output
            DataFrame.
        index
            One or multiple keys to group by. If None, all remaining columns not specified
            on `on` and `values` will be used. At least one of `index` and `values` must
            be specified.
        values
            One or multiple keys to group by. If None, all remaining columns not specified
            on `on` and `index` will be used. At least one of `index` and `values` must
            be specified.
        aggregate_function
            Choose from:

            - None: no aggregation takes place, will raise error if multiple values are in group.
            - A predefined aggregate function string, one of
              {'min', 'max', 'first', 'last', 'sum', 'mean', 'median', 'len'}
            - An expression to do the aggregation.
        maintain_order
            Sort the grouped keys so that the output order is predictable.
        sort_columns
            Sort the transposed columns by name. Default is by order of discovery.
        separator
            Used as separator/delimiter in generated column names in case of multiple
            `values` columns.

        Returns
        -------
        DataFrame

        Notes
        -----
        In some other frameworks, you might know this operation as `pivot_wider`.

        Examples
        --------
        You can use `pivot` to reshape a dataframe from "long" to "wide" format.

        For example, suppose we have a dataframe of test scores achieved by some
        students, where each row represents a distinct test.

        >>> df = pl.DataFrame(
        ...     {
        ...         "name": ["Cady", "Cady", "Karen", "Karen"],
        ...         "subject": ["maths", "physics", "maths", "physics"],
        ...         "test_1": [98, 99, 61, 58],
        ...         "test_2": [100, 100, 60, 60],
        ...     }
        ... )
        >>> df
        shape: (4, 4)
        ┌───────┬─────────┬────────┬────────┐
        │ name  ┆ subject ┆ test_1 ┆ test_2 │
        │ ---   ┆ ---     ┆ ---    ┆ ---    │
        │ str   ┆ str     ┆ i64    ┆ i64    │
        ╞═══════╪═════════╪════════╪════════╡
        │ Cady  ┆ maths   ┆ 98     ┆ 100    │
        │ Cady  ┆ physics ┆ 99     ┆ 100    │
        │ Karen ┆ maths   ┆ 61     ┆ 60     │
        │ Karen ┆ physics ┆ 58     ┆ 60     │
        └───────┴─────────┴────────┴────────┘

        Using `pivot`, we can reshape so we have one row per student, with different
        subjects as columns, and their `test_1` scores as values:

        >>> df.pivot("subject", index="name", values="test_1")
        shape: (2, 3)
        ┌───────┬───────┬─────────┐
        │ name  ┆ maths ┆ physics │
        │ ---   ┆ ---   ┆ ---     │
        │ str   ┆ i64   ┆ i64     │
        ╞═══════╪═══════╪═════════╡
        │ Cady  ┆ 98    ┆ 99      │
        │ Karen ┆ 61    ┆ 58      │
        └───────┴───────┴─────────┘

        You can use selectors too - here we include all test scores in the pivoted table:

        >>> import polars.selectors as cs
        >>> df.pivot("subject", values=cs.starts_with("test"))
        shape: (2, 5)
        ┌───────┬──────────────┬────────────────┬──────────────┬────────────────┐
        │ name  ┆ test_1_maths ┆ test_1_physics ┆ test_2_maths ┆ test_2_physics │
        │ ---   ┆ ---          ┆ ---            ┆ ---          ┆ ---            │
        │ str   ┆ i64          ┆ i64            ┆ i64          ┆ i64            │
        ╞═══════╪══════════════╪════════════════╪══════════════╪════════════════╡
        │ Cady  ┆ 98           ┆ 99             ┆ 100          ┆ 100            │
        │ Karen ┆ 61           ┆ 58             ┆ 60           ┆ 60             │
        └───────┴──────────────┴────────────────┴──────────────┴────────────────┘

        If you end up with multiple values per cell, you can specify how to aggregate
        them with `aggregate_function`:

        >>> df = pl.DataFrame(
        ...     {
        ...         "ix": [1, 1, 2, 2, 1, 2],
        ...         "col": ["a", "a", "a", "a", "b", "b"],
        ...         "foo": [0, 1, 2, 2, 7, 1],
        ...         "bar": [0, 2, 0, 0, 9, 4],
        ...     }
        ... )
        >>> df.pivot("col", index="ix", aggregate_function="sum")
        shape: (2, 5)
        ┌─────┬───────┬───────┬───────┬───────┐
        │ ix  ┆ foo_a ┆ foo_b ┆ bar_a ┆ bar_b │
        │ --- ┆ ---   ┆ ---   ┆ ---   ┆ ---   │
        │ i64 ┆ i64   ┆ i64   ┆ i64   ┆ i64   │
        ╞═════╪═══════╪═══════╪═══════╪═══════╡
        │ 1   ┆ 1     ┆ 7     ┆ 2     ┆ 9     │
        │ 2   ┆ 4     ┆ 1     ┆ 0     ┆ 4     │
        └─────┴───────┴───────┴───────┴───────┘

        You can also pass a custom aggregation function using
        :meth:`polars.element`:

        >>> df = pl.DataFrame(
        ...     {
        ...         "col1": ["a", "a", "a", "b", "b", "b"],
        ...         "col2": ["x", "x", "x", "x", "y", "y"],
        ...         "col3": [6, 7, 3, 2, 5, 7],
        ...     }
        ... )
        >>> df.pivot(
        ...     "col2",
        ...     index="col1",
        ...     values="col3",
        ...     aggregate_function=pl.element().tanh().mean(),
        ... )
        shape: (2, 3)
        ┌──────┬──────────┬──────────┐
        │ col1 ┆ x        ┆ y        │
        │ ---  ┆ ---      ┆ ---      │
        │ str  ┆ f64      ┆ f64      │
        ╞══════╪══════════╪══════════╡
        │ a    ┆ 0.998347 ┆ null     │
        │ b    ┆ 0.964028 ┆ 0.999954 │
        └──────┴──────────┴──────────┘

        Note that `pivot` is only available in eager mode. If you know the unique
        column values in advance, you can use :meth:`polars.LazyFrame.group_by` to
        get the same result as above in lazy mode:

        >>> index = pl.col("col1")
        >>> on = pl.col("col2")
        >>> values = pl.col("col3")
        >>> unique_column_values = ["x", "y"]
        >>> aggregate_function = lambda col: col.tanh().mean()
        >>> df.lazy().group_by(index).agg(
        ...     aggregate_function(values.filter(on == value)).alias(value)
        ...     for value in unique_column_values
        ... ).collect()  # doctest: +IGNORE_RESULT
        shape: (2, 3)
        ┌──────┬──────────┬──────────┐
        │ col1 ┆ x        ┆ y        │
        │ ---  ┆ ---      ┆ ---      │
        │ str  ┆ f64      ┆ f64      │
        ╞══════╪══════════╪══════════╡
        │ a    ┆ 0.998347 ┆ null     │
        │ b    ┆ 0.964028 ┆ 0.999954 │
        └──────┴──────────┴──────────┘
        """  # noqa: W505
        on = _expand_selectors(self, on)
        if values is not None:
            values = _expand_selectors(self, values)
        if index is not None:
            index = _expand_selectors(self, index)

        if isinstance(aggregate_function, str):
            if aggregate_function == "first":
                aggregate_expr = F.element().first()._pyexpr
            elif aggregate_function == "sum":
                aggregate_expr = F.element().sum()._pyexpr
            elif aggregate_function == "max":
                aggregate_expr = F.element().max()._pyexpr
            elif aggregate_function == "min":
                aggregate_expr = F.element().min()._pyexpr
            elif aggregate_function == "mean":
                aggregate_expr = F.element().mean()._pyexpr
            elif aggregate_function == "median":
                aggregate_expr = F.element().median()._pyexpr
            elif aggregate_function == "last":
                aggregate_expr = F.element().last()._pyexpr
            elif aggregate_function == "len":
                aggregate_expr = F.len()._pyexpr
            elif aggregate_function == "count":
                issue_deprecation_warning(
                    "`aggregate_function='count'` input for `pivot` is deprecated."
                    " Please use `aggregate_function='len'`.",
                    version="0.20.5",
                )
                aggregate_expr = F.len()._pyexpr
            else:
                msg = f"invalid input for `aggregate_function` argument: {aggregate_function!r}"
                raise ValueError(msg)
        elif aggregate_function is None:
            aggregate_expr = None
        else:
            aggregate_expr = aggregate_function._pyexpr

        return self._from_pydf(
            self._df.pivot_expr(
                on,
                index,
                values,
                maintain_order,
                sort_columns,
                aggregate_expr,
                separator,
            )
        )
