    def replace_strict(
        self,
        old: IntoExpr | Sequence[Any] | Mapping[Any, Any],
        new: IntoExpr | Sequence[Any] | NoDefault = no_default,
        *,
        default: IntoExpr | NoDefault = no_default,
        return_dtype: PolarsDataType | None = None,
    ) -> Expr:
        """
        Replace all values by different values.

        Parameters
        ----------
        old
            Value or sequence of values to replace.
            Accepts expression input. Sequences are parsed as Series,
            other non-expression inputs are parsed as literals.
            Also accepts a mapping of values to their replacement as syntactic sugar for
            `replace_all(old=Series(mapping.keys()), new=Series(mapping.values()))`.
        new
            Value or sequence of values to replace by.
            Accepts expression input. Sequences are parsed as Series,
            other non-expression inputs are parsed as literals.
            Length must match the length of `old` or have length 1.
        default
            Set values that were not replaced to this value. If no default is specified,
            (default), an error is raised if any values were not replaced.
            Accepts expression input. Non-expression inputs are parsed as literals.
        return_dtype
            The data type of the resulting expression. If set to `None` (default),
            the data type is determined automatically based on the other inputs.

        Raises
        ------
        InvalidOperationError
            If any non-null values in the original column were not replaced, and no
            `default` was specified.

        See Also
        --------
        replace
        str.replace

        Notes
        -----
        The global string cache must be enabled when replacing categorical values.

        Examples
        --------
        Replace values by passing sequences to the `old` and `new` parameters.

        >>> df = pl.DataFrame({"a": [1, 2, 2, 3]})
        >>> df.with_columns(
        ...     replaced=pl.col("a").replace_strict([1, 2, 3], [100, 200, 300])
        ... )
        shape: (4, 2)
        ┌─────┬──────────┐
        │ a   ┆ replaced │
        │ --- ┆ ---      │
        │ i64 ┆ i64      │
        ╞═════╪══════════╡
        │ 1   ┆ 100      │
        │ 2   ┆ 200      │
        │ 2   ┆ 200      │
        │ 3   ┆ 300      │
        └─────┴──────────┘

        Passing a mapping with replacements is also supported as syntactic sugar.

        >>> mapping = {1: 100, 2: 200, 3: 300}
        >>> df.with_columns(replaced=pl.col("a").replace_strict(mapping))
        shape: (4, 2)
        ┌─────┬──────────┐
        │ a   ┆ replaced │
        │ --- ┆ ---      │
        │ i64 ┆ i64      │
        ╞═════╪══════════╡
        │ 1   ┆ 100      │
        │ 2   ┆ 200      │
        │ 2   ┆ 200      │
        │ 3   ┆ 300      │
        └─────┴──────────┘

        By default, an error is raised if any non-null values were not replaced.
        Specify a default to set all values that were not matched.

        >>> mapping = {2: 200, 3: 300}
        >>> df.with_columns(
        ...     replaced=pl.col("a").replace_strict(mapping)
        ... )  # doctest: +SKIP
        Traceback (most recent call last):
        ...
        polars.exceptions.InvalidOperationError: incomplete mapping specified for `replace_strict`
        >>> df.with_columns(replaced=pl.col("a").replace_strict(mapping, default=-1))
        shape: (4, 2)
        ┌─────┬──────────┐
        │ a   ┆ replaced │
        │ --- ┆ ---      │
        │ i64 ┆ i64      │
        ╞═════╪══════════╡
        │ 1   ┆ -1       │
        │ 2   ┆ 200      │
        │ 2   ┆ 200      │
        │ 3   ┆ 300      │
        └─────┴──────────┘

        Replacing by values of a different data type sets the return type based on
        a combination of the `new` data type and the `default` data type.

        >>> df = pl.DataFrame({"a": ["x", "y", "z"]})
        >>> mapping = {"x": 1, "y": 2, "z": 3}
        >>> df.with_columns(replaced=pl.col("a").replace_strict(mapping))
        shape: (3, 2)
        ┌─────┬──────────┐
        │ a   ┆ replaced │
        │ --- ┆ ---      │
        │ str ┆ i64      │
        ╞═════╪══════════╡
        │ x   ┆ 1        │
        │ y   ┆ 2        │
        │ z   ┆ 3        │
        └─────┴──────────┘
        >>> df.with_columns(replaced=pl.col("a").replace_strict(mapping, default="x"))
        shape: (3, 2)
        ┌─────┬──────────┐
        │ a   ┆ replaced │
        │ --- ┆ ---      │
        │ str ┆ str      │
        ╞═════╪══════════╡
        │ x   ┆ 1        │
        │ y   ┆ 2        │
        │ z   ┆ 3        │
        └─────┴──────────┘

        Set the `return_dtype` parameter to control the resulting data type directly.

        >>> df.with_columns(
        ...     replaced=pl.col("a").replace_strict(mapping, return_dtype=pl.UInt8)
        ... )
        shape: (3, 2)
        ┌─────┬──────────┐
        │ a   ┆ replaced │
        │ --- ┆ ---      │
        │ str ┆ u8       │
        ╞═════╪══════════╡
        │ x   ┆ 1        │
        │ y   ┆ 2        │
        │ z   ┆ 3        │
        └─────┴──────────┘

        Expression input is supported for all parameters.

        >>> df = pl.DataFrame({"a": [1, 2, 2, 3], "b": [1.5, 2.5, 5.0, 1.0]})
        >>> df.with_columns(
        ...     replaced=pl.col("a").replace_strict(
        ...         old=pl.col("a").max(),
        ...         new=pl.col("b").sum(),
        ...         default=pl.col("b"),
        ...     )
        ... )
        shape: (4, 3)
        ┌─────┬─────┬──────────┐
        │ a   ┆ b   ┆ replaced │
        │ --- ┆ --- ┆ ---      │
        │ i64 ┆ f64 ┆ f64      │
        ╞═════╪═════╪══════════╡
        │ 1   ┆ 1.5 ┆ 1.5      │
        │ 2   ┆ 2.5 ┆ 2.5      │
        │ 2   ┆ 5.0 ┆ 5.0      │
        │ 3   ┆ 1.0 ┆ 10.0     │
        └─────┴─────┴──────────┘
        """  # noqa: W505
        if new is no_default and isinstance(old, Mapping):
            new = pl.Series(old.values())
            old = pl.Series(old.keys())

        old = parse_into_expression(old, str_as_lit=True, list_as_series=True)  # type: ignore[arg-type]
        new = parse_into_expression(new, str_as_lit=True, list_as_series=True)  # type: ignore[arg-type]

        default = (
            None
            if default is no_default
            else parse_into_expression(default, str_as_lit=True)
        )

        return self._from_pyexpr(
            self._pyexpr.replace_strict(old, new, default, return_dtype)
        )
