    def when(
        self,
        *predicates: IntoExpr | Iterable[IntoExpr],
        **constraints: Any,
    ) -> ChainedWhen:
        """
        Add another condition to the `when-then-otherwise` expression.

        Parameters
        ----------
        predicates
            Condition(s) that must be met in order to apply the subsequent statement.
            Accepts one or more boolean expressions, which are implicitly combined with
            `&`. String input is parsed as a column name.
        constraints
            Apply conditions as `col_name = value` keyword arguments that are treated as
            equality matches, such as `x = 123`. As with the predicates parameter,
            multiple conditions are implicitly combined using `&`.
        """
        condition_pyexpr = parse_predicates_constraints_into_expression(
            *predicates, **constraints
        )
        return ChainedWhen(self._chained_then.when(condition_pyexpr))
