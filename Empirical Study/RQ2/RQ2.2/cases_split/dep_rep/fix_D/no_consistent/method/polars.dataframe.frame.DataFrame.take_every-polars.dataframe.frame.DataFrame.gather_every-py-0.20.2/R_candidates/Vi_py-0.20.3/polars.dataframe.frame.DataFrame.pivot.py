    def pivot(
        self,
        values: ColumnNameOrSelector | Sequence[ColumnNameOrSelector] | None,
        index: ColumnNameOrSelector | Sequence[ColumnNameOrSelector] | None,
        columns: ColumnNameOrSelector | Sequence[ColumnNameOrSelector] | None,
        aggregate_function: PivotAgg | Expr | None = None,
        *,
        maintain_order: bool = True,
        sort_columns: bool = False,
        separator: str = "_",
    ) -> Self:
        """
        Create a spreadsheet-style pivot table as a DataFrame.

        Only available in eager mode. See "Examples" section below for how to do a
        "lazy pivot" if you know the unique column values in advance.

        Parameters
        ----------
        values
            Column values to aggregate. Can be multiple columns if the *columns*
            arguments contains multiple columns as well.
        index
            One or multiple keys to group by.
        columns
            Name of the column(s) whose values will be used as the header of the output
            DataFrame.
        aggregate_function
            Choose from:

            - None: no aggregation takes place, will raise error if multiple values are in group.
            - A predefined aggregate function string, one of
              {'first', 'sum', 'max', 'min', 'mean', 'median', 'last', 'count'}
            - An expression to do the aggregation.

        maintain_order
            Sort the grouped keys so that the output order is predictable.
        sort_columns
            Sort the transposed columns by name. Default is by order of discovery.
        separator
            Used as separator/delimiter in generated column names.

        Returns
        -------
        DataFrame

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "foo": ["one", "one", "two", "two", "one", "two"],
        ...         "bar": ["y", "y", "y", "x", "x", "x"],
        ...         "baz": [1, 2, 3, 4, 5, 6],
        ...     }
        ... )
        >>> df.pivot(values="baz", index="foo", columns="bar", aggregate_function="sum")
        shape: (2, 3)
        ┌─────┬─────┬─────┐
        │ foo ┆ y   ┆ x   │
        │ --- ┆ --- ┆ --- │
        │ str ┆ i64 ┆ i64 │
        ╞═════╪═════╪═════╡
        │ one ┆ 3   ┆ 5   │
        │ two ┆ 3   ┆ 10  │
        └─────┴─────┴─────┘

        Pivot using selectors to determine the index/values/columns:

        >>> import polars.selectors as cs
        >>> df.pivot(
        ...     values=cs.numeric(),
        ...     index=cs.string(),
        ...     columns=cs.string(),
        ...     aggregate_function="sum",
        ...     sort_columns=True,
        ... ).sort(
        ...     by=cs.string(),
        ... )
        shape: (4, 6)
        ┌─────┬─────┬──────┬──────┬──────┬──────┐
        │ foo ┆ bar ┆ one  ┆ two  ┆ x    ┆ y    │
        │ --- ┆ --- ┆ ---  ┆ ---  ┆ ---  ┆ ---  │
        │ str ┆ str ┆ i64  ┆ i64  ┆ i64  ┆ i64  │
        ╞═════╪═════╪══════╪══════╪══════╪══════╡
        │ one ┆ x   ┆ 5    ┆ null ┆ 5    ┆ null │
        │ one ┆ y   ┆ 3    ┆ null ┆ null ┆ 3    │
        │ two ┆ x   ┆ null ┆ 10   ┆ 10   ┆ null │
        │ two ┆ y   ┆ null ┆ 3    ┆ null ┆ 3    │
        └─────┴─────┴──────┴──────┴──────┴──────┘

        Run an expression as aggregation function

        >>> df = pl.DataFrame(
        ...     {
        ...         "col1": ["a", "a", "a", "b", "b", "b"],
        ...         "col2": ["x", "x", "x", "x", "y", "y"],
        ...         "col3": [6, 7, 3, 2, 5, 7],
        ...     }
        ... )
        >>> df.pivot(
        ...     index="col1",
        ...     columns="col2",
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
        column values in advance, you can use :meth:`polars.LazyFrame.groupby` to
        get the same result as above in lazy mode:

        >>> index = pl.col("col1")
        >>> columns = pl.col("col2")
        >>> values = pl.col("col3")
        >>> unique_column_values = ["x", "y"]
        >>> aggregate_function = lambda col: col.tanh().mean()
        >>> (
        ...     df.lazy()
        ...     .group_by(index)
        ...     .agg(
        ...         *[
        ...             aggregate_function(values.filter(columns == value)).alias(value)
        ...             for value in unique_column_values
        ...         ]
        ...     )
        ...     .collect()
        ... )  # doctest: +IGNORE_RESULT
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
        values = _expand_selectors(self, values)
        index = _expand_selectors(self, index)
        columns = _expand_selectors(self, columns)

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
            elif aggregate_function == "count":
                aggregate_expr = F.count()._pyexpr
            else:
                raise ValueError(
                    f"invalid input for `aggregate_function` argument: {aggregate_function!r}"
                )
        elif aggregate_function is None:
            aggregate_expr = None
        else:
            aggregate_expr = aggregate_function._pyexpr

        return self._from_pydf(
            self._df.pivot_expr(
                values,
                index,
                columns,
                maintain_order,
                sort_columns,
                aggregate_expr,
                separator,
            )
        )
