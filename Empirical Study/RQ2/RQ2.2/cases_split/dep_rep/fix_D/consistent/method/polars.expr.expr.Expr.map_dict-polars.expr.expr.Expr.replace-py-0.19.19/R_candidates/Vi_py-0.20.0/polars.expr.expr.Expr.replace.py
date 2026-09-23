    def replace(
        self,
        old: IntoExpr | Sequence[Any] | Mapping[Any, Any],
        new: IntoExpr | Sequence[Any] | NoDefault = no_default,
        *,
        default: IntoExpr | NoDefault = no_default,
        return_dtype: PolarsDataType | None = None,
    ) -> Self:
        """
        Replace values by different values.

        Parameters
        ----------
        old
            Value or sequence of values to replace.
            Accepts expression input. Sequences are parsed as Series,
            other non-expression inputs are parsed as literals.
            Also accepts a mapping of values to their replacement as syntactic sugar for
            `replace(new=Series(mapping.keys()), old=Series(mapping.values()))`.
        new
            Value or sequence of values to replace by.
            Accepts expression input. Sequences are parsed as Series,
            other non-expression inputs are parsed as literals.
            Length must match the length of `old` or have length 1.
        default
            Set values that were not replaced to this value.
            Defaults to keeping the original value.
            Accepts expression input. Non-expression inputs are parsed as literals.
        return_dtype
            The data type of the resulting expression. If set to `None` (default),
            the data type is determined automatically based on the other inputs.

        See Also
        --------
        str.replace

        Notes
        -----
        The global string cache must be enabled when replacing categorical values.

        Examples
        --------
        Replace a single value by another value. Values that were not replaced remain
        unchanged.

        >>> df = pl.DataFrame({"a": [1, 2, 2, 3]})
        >>> df.with_columns(replaced=pl.col("a").replace(2, 100))
        shape: (4, 2)
        ┌─────┬──────────┐
        │ a   ┆ replaced │
        │ --- ┆ ---      │
        │ i64 ┆ i64      │
        ╞═════╪══════════╡
        │ 1   ┆ 1        │
        │ 2   ┆ 100      │
        │ 2   ┆ 100      │
        │ 3   ┆ 3        │
        └─────┴──────────┘

        Replace multiple values by passing sequences to the `old` and `new` parameters.

        >>> df.with_columns(replaced=pl.col("a").replace([2, 3], [100, 200]))
        shape: (4, 2)
        ┌─────┬──────────┐
        │ a   ┆ replaced │
        │ --- ┆ ---      │
        │ i64 ┆ i64      │
        ╞═════╪══════════╡
        │ 1   ┆ 1        │
        │ 2   ┆ 100      │
        │ 2   ┆ 100      │
        │ 3   ┆ 200      │
        └─────┴──────────┘

        Passing a mapping with replacements is also supported as syntactic sugar.
        Specify a default to set all values that were not matched.

        >>> mapping = {2: 100, 3: 200}
        >>> df.with_columns(replaced=pl.col("a").replace(mapping, default=-1))
        shape: (4, 2)
        ┌─────┬──────────┐
        │ a   ┆ replaced │
        │ --- ┆ ---      │
        │ i64 ┆ i64      │
        ╞═════╪══════════╡
        │ 1   ┆ -1       │
        │ 2   ┆ 100      │
        │ 2   ┆ 100      │
        │ 3   ┆ 200      │
        └─────┴──────────┘

        Replacing by values of a different data type sets the return type based on
        a combination of the `new` data type and either the original data type or the
        default data type if it was set.

        >>> df = pl.DataFrame({"a": ["x", "y", "z"]})
        >>> mapping = {"x": 1, "y": 2, "z": 3}
        >>> df.with_columns(replaced=pl.col("a").replace(mapping))
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
        >>> df.with_columns(replaced=pl.col("a").replace(mapping, default=None))
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

        Set the `return_dtype` parameter to control the resulting data type directly.

        >>> df.with_columns(
        ...     replaced=pl.col("a").replace(mapping, return_dtype=pl.UInt8)
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
        ...     replaced=pl.col("a").replace(
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
        """
        if new is no_default and isinstance(old, Mapping):
            new = pl.Series(old.values())
            old = pl.Series(old.keys())
        else:
            if isinstance(old, Sequence) and not isinstance(old, (str, pl.Series)):
                old = pl.Series(old)
            if isinstance(new, Sequence) and not isinstance(new, (str, pl.Series)):
                new = pl.Series(new)

        old = parse_as_expression(old, str_as_lit=True)  # type: ignore[arg-type]
        new = parse_as_expression(new, str_as_lit=True)  # type: ignore[arg-type]

        default = (
            None
            if default is no_default
            else parse_as_expression(default, str_as_lit=True)
        )

        return self._from_pyexpr(self._pyexpr.replace(old, new, default, return_dtype))
