    def with_fields(
        self,
        *exprs: IntoExpr | Iterable[IntoExpr],
        **named_exprs: IntoExpr,
    ) -> Expr:
        """
        Add or overwrite fields of this struct.

        This is similar to `with_columns` on `DataFrame`.

        .. versionadded:: 0.20.27

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "coords": [{"x": 1, "y": 4}, {"x": 4, "y": 9}, {"x": 9, "y": 16}],
        ...         "multiply": [10, 2, 3],
        ...     }
        ... )
        >>> df
        shape: (3, 2)
        ┌───────────┬──────────┐
        │ coords    ┆ multiply │
        │ ---       ┆ ---      │
        │ struct[2] ┆ i64      │
        ╞═══════════╪══════════╡
        │ {1,4}     ┆ 10       │
        │ {4,9}     ┆ 2        │
        │ {9,16}    ┆ 3        │
        └───────────┴──────────┘
        >>> df = df.with_columns(
        ...     pl.col("coords").struct.with_fields(
        ...         pl.field("x").sqrt(),
        ...         y_mul=pl.field("y") * pl.col("multiply"),
        ...     )
        ... )
        >>> df
        shape: (3, 2)
        ┌─────────────┬──────────┐
        │ coords      ┆ multiply │
        │ ---         ┆ ---      │
        │ struct[3]   ┆ i64      │
        ╞═════════════╪══════════╡
        │ {1.0,4,40}  ┆ 10       │
        │ {2.0,9,18}  ┆ 2        │
        │ {3.0,16,48} ┆ 3        │
        └─────────────┴──────────┘
        >>> df.unnest("coords")
        shape: (3, 4)
        ┌─────┬─────┬───────┬──────────┐
        │ x   ┆ y   ┆ y_mul ┆ multiply │
        │ --- ┆ --- ┆ ---   ┆ ---      │
        │ f64 ┆ i64 ┆ i64   ┆ i64      │
        ╞═════╪═════╪═══════╪══════════╡
        │ 1.0 ┆ 4   ┆ 40    ┆ 10       │
        │ 2.0 ┆ 9   ┆ 18    ┆ 2        │
        │ 3.0 ┆ 16  ┆ 48    ┆ 3        │
        └─────┴─────┴───────┴──────────┘

        Parameters
        ----------
        *exprs
            Field(s) to add, specified as positional arguments.
            Accepts expression input. Strings are parsed as column names, other
            non-expression inputs are parsed as literals.
        **named_exprs
            Additional fields to add, specified as keyword arguments.
            The columns will be renamed to the keyword used.

        See Also
        --------
        field
        """
        structify = bool(int(os.environ.get("POLARS_AUTO_STRUCTIFY", 0)))

        pyexprs = parse_as_list_of_expressions(
            *exprs, **named_exprs, __structify=structify
        )

        return wrap_expr(self._pyexpr.struct_with_fields(pyexprs))
