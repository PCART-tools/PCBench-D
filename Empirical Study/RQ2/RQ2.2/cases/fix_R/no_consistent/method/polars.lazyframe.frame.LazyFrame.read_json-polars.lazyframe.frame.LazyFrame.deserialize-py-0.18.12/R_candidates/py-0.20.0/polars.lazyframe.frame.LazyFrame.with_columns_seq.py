    def with_columns_seq(
        self,
        *exprs: IntoExpr | Iterable[IntoExpr],
        **named_exprs: IntoExpr,
    ) -> Self:
        """
        Add columns to this DataFrame.

        Added columns will replace existing columns with the same name.

        This will run all expression sequentially instead of in parallel.
        Use this when the work per expression is cheap.

        Parameters
        ----------
        *exprs
            Column(s) to add, specified as positional arguments.
            Accepts expression input. Strings are parsed as column names, other
            non-expression inputs are parsed as literals.
        **named_exprs
            Additional columns to add, specified as keyword arguments.
            The columns will be renamed to the keyword used.

        Returns
        -------
        LazyFrame
            A new LazyFrame with the columns added.

        See Also
        --------
        with_columns

        """
        structify = bool(int(os.environ.get("POLARS_AUTO_STRUCTIFY", 0)))

        pyexprs = parse_as_list_of_expressions(
            *exprs, **named_exprs, __structify=structify
        )
        return self._from_pyldf(self._ldf.with_columns_seq(pyexprs))
