    def replace(
        self,
        old: IntoExpr | Sequence[Any] | Mapping[Any, Any],
        new: IntoExpr | Sequence[Any] | NoDefault = no_default,
        *,
        default: IntoExpr | NoDefault = no_default,
        return_dtype: PolarsDataType | None = None,
    ) -> Expr:
        """
        Replace the given values by different values of the same data type.

        Parameters
        ----------
        old
            Value or sequence of values to replace.
            Accepts expression input. Sequences are parsed as Series,
            other non-expression inputs are parsed as literals.
            Also accepts a mapping of values to their replacement as syntactic sugar for
            `replace(old=Series(mapping.keys()), new=Series(mapping.values()))`.
        new
            Value or sequence of values to replace by.
            Accepts expression input. Sequences are parsed as Series,
            other non-expression inputs are parsed as literals.
            Length must match the length of `old` or have length 1.

        default
            Set values that were not replaced to this value.
            Defaults to keeping the original value.
            Accepts expression input. Non-expression inputs are parsed as literals.

            .. deprecated:: 1.0.0
                Use :meth:`replace_strict` instead to set a default while replacing
                values.

        return_dtype
            The data type of the resulting expression. If set to `None` (default),
            the data type of the original column is preserved.

            .. deprecated:: 1.0.0
                Use :meth:`replace_strict` instead to set a return data type while
                replacing values, or explicitly call :meth:`cast` on the output.

        See Also
        --------
        replace_strict
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

        >>> mapping = {2: 100, 3: 200}
        >>> df.with_columns(replaced=pl.col("a").replace(mapping))
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

        The original data type is preserved when replacing by values of a different
        data type. Use :meth:`replace_strict` to replace and change the return data
        type.

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

        Expression input is supported.

        >>> df = pl.DataFrame({"a": [1, 2, 2, 3], "b": [1.5, 2.5, 5.0, 1.0]})
        >>> df.with_columns(
        ...     replaced=pl.col("a").replace(
        ...         old=pl.col("a").max(),
        ...         new=pl.col("b").sum(),
        ...     )
        ... )
        shape: (4, 3)
        ┌─────┬─────┬──────────┐
        │ a   ┆ b   ┆ replaced │
        │ --- ┆ --- ┆ ---      │
        │ i64 ┆ f64 ┆ i64      │
        ╞═════╪═════╪══════════╡
        │ 1   ┆ 1.5 ┆ 1        │
        │ 2   ┆ 2.5 ┆ 2        │
        │ 2   ┆ 5.0 ┆ 2        │
        │ 3   ┆ 1.0 ┆ 10       │
        └─────┴─────┴──────────┘
        """
        if return_dtype is not None:
            issue_deprecation_warning(
                "The `return_dtype` parameter for `replace` is deprecated."
                " Use `replace_strict` instead to set a return data type while replacing values.",
                version="1.0.0",
            )
        if default is not no_default:
            issue_deprecation_warning(
                "The `default` parameter for `replace` is deprecated."
                " Use `replace_strict` instead to set a default while replacing values.",
                version="1.0.0",
            )
            return self.replace_strict(
                old, new, default=default, return_dtype=return_dtype
            )

        if new is no_default and isinstance(old, Mapping):
            new = pl.Series(old.values())
            old = pl.Series(old.keys())
        else:
            if isinstance(old, Sequence) and not isinstance(old, (str, pl.Series)):
                old = pl.Series(old)
            if isinstance(new, Sequence) and not isinstance(new, (str, pl.Series)):
                new = pl.Series(new)

        old = parse_into_expression(old, str_as_lit=True)  # type: ignore[arg-type]
        new = parse_into_expression(new, str_as_lit=True)  # type: ignore[arg-type]

        result = self._from_pyexpr(self._pyexpr.replace(old, new))

        if return_dtype is not None:
            result = result.cast(return_dtype)

        return result
