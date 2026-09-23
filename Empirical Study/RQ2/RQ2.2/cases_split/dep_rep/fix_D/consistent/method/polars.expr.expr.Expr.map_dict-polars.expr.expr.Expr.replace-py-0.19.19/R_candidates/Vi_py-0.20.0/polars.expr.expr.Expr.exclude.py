    def exclude(
        self,
        columns: str | PolarsDataType | Collection[str] | Collection[PolarsDataType],
        *more_columns: str | PolarsDataType,
    ) -> Self:
        """
        Exclude columns from a multi-column expression.

        Only works after a wildcard or regex column selection, and you cannot provide
        both string column names *and* dtypes (you may prefer to use selectors instead).

        Parameters
        ----------
        columns
            The name or datatype of the column(s) to exclude. Accepts regular expression
            input. Regular expressions should start with `^` and end with `$`.
        *more_columns
            Additional names or datatypes of columns to exclude, specified as positional
            arguments.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "aa": [1, 2, 3],
        ...         "ba": ["a", "b", None],
        ...         "cc": [None, 2.5, 1.5],
        ...     }
        ... )
        >>> df
        shape: (3, 3)
        ┌─────┬──────┬──────┐
        │ aa  ┆ ba   ┆ cc   │
        │ --- ┆ ---  ┆ ---  │
        │ i64 ┆ str  ┆ f64  │
        ╞═════╪══════╪══════╡
        │ 1   ┆ a    ┆ null │
        │ 2   ┆ b    ┆ 2.5  │
        │ 3   ┆ null ┆ 1.5  │
        └─────┴──────┴──────┘

        Exclude by column name(s):

        >>> df.select(pl.all().exclude("ba"))
        shape: (3, 2)
        ┌─────┬──────┐
        │ aa  ┆ cc   │
        │ --- ┆ ---  │
        │ i64 ┆ f64  │
        ╞═════╪══════╡
        │ 1   ┆ null │
        │ 2   ┆ 2.5  │
        │ 3   ┆ 1.5  │
        └─────┴──────┘

        Exclude by regex, e.g. removing all columns whose names end with the letter "a":

        >>> df.select(pl.all().exclude("^.*a$"))
        shape: (3, 1)
        ┌──────┐
        │ cc   │
        │ ---  │
        │ f64  │
        ╞══════╡
        │ null │
        │ 2.5  │
        │ 1.5  │
        └──────┘

        Exclude by dtype(s), e.g. removing all columns of type Int64 or Float64:

        >>> df.select(pl.all().exclude([pl.Int64, pl.Float64]))
        shape: (3, 1)
        ┌──────┐
        │ ba   │
        │ ---  │
        │ str  │
        ╞══════╡
        │ a    │
        │ b    │
        │ null │
        └──────┘

        """
        exclude_cols: list[str] = []
        exclude_dtypes: list[PolarsDataType] = []
        for item in (
            *(
                columns
                if isinstance(columns, Collection) and not isinstance(columns, str)
                else [columns]
            ),
            *more_columns,
        ):
            if isinstance(item, str):
                exclude_cols.append(item)
            elif is_polars_dtype(item):
                exclude_dtypes.append(item)
            else:
                raise TypeError(
                    "invalid input for `exclude`"
                    f"\n\nExpected one or more `str`, `DataType`, or selector; found {type(item).__name__!r} instead."
                )

        if exclude_cols and exclude_dtypes:
            raise TypeError(
                "cannot exclude by both column name and dtype; use a selector instead"
            )
        elif exclude_dtypes:
            return self._from_pyexpr(self._pyexpr.exclude_dtype(exclude_dtypes))
        else:
            return self._from_pyexpr(self._pyexpr.exclude(exclude_cols))
