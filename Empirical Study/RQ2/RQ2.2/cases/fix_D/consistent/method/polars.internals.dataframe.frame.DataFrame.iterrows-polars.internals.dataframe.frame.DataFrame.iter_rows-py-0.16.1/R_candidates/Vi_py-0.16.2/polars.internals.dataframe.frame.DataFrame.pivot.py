    def pivot(
        self: DF,
        values: Sequence[str] | str,
        index: Sequence[str] | str,
        columns: Sequence[str] | str,
        aggregate_fn: PivotAgg | pli.Expr = "first",
        maintain_order: bool = True,
        sort_columns: bool = False,
    ) -> DF:
        """
        Create a spreadsheet-style pivot table as a DataFrame.

        Parameters
        ----------
        values
            Column values to aggregate. Can be multiple columns if the *columns*
            arguments contains multiple columns as well
        index
            One or multiple keys to group by
        columns
            Columns whose values will be used as the header of the output DataFrame
        aggregate_fn : {'first', 'sum', 'max', 'min', 'mean', 'median', 'last', 'count'}
            A predefined aggregate function str or an expression.
        maintain_order
            Sort the grouped keys so that the output order is predictable.
        sort_columns
            Sort the transposed columns by name. Default is by order of discovery.

        Returns
        -------
        DataFrame

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "foo": ["one", "one", "one", "two", "two", "two"],
        ...         "bar": ["A", "B", "C", "A", "B", "C"],
        ...         "baz": [1, 2, 3, 4, 5, 6],
        ...     }
        ... )
        >>> df.pivot(values="baz", index="foo", columns="bar")
        shape: (2, 4)
        ┌─────┬─────┬─────┬─────┐
        │ foo ┆ A   ┆ B   ┆ C   │
        │ --- ┆ --- ┆ --- ┆ --- │
        │ str ┆ i64 ┆ i64 ┆ i64 │
        ╞═════╪═════╪═════╪═════╡
        │ one ┆ 1   ┆ 2   ┆ 3   │
        │ two ┆ 4   ┆ 5   ┆ 6   │
        └─────┴─────┴─────┴─────┘

        """
        if isinstance(values, str):
            values = [values]
        if isinstance(index, str):
            index = [index]
        if isinstance(columns, str):
            columns = [columns]

        if isinstance(aggregate_fn, str):
            if aggregate_fn == "first":
                aggregate_fn = pli.element().first()
            elif aggregate_fn == "sum":
                aggregate_fn = pli.element().sum()
            elif aggregate_fn == "max":
                aggregate_fn = pli.element().max()
            elif aggregate_fn == "min":
                aggregate_fn = pli.element().min()
            elif aggregate_fn == "mean":
                aggregate_fn = pli.element().mean()
            elif aggregate_fn == "median":
                aggregate_fn = pli.element().median()
            elif aggregate_fn == "last":
                aggregate_fn = pli.element().last()
            elif aggregate_fn == "count":
                aggregate_fn = pli.count()
            else:
                raise ValueError(
                    f"Argument aggregate fn: '{aggregate_fn}' " f"was not expected."
                )

        return self._from_pydf(
            self._df.pivot_expr(
                values,
                index,
                columns,
                aggregate_fn._pyexpr,
                maintain_order,
                sort_columns,
            )
        )
