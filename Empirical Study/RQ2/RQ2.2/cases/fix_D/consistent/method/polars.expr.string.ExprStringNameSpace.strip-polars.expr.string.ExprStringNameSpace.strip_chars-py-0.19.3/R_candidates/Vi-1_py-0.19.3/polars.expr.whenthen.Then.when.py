    @deprecate_renamed_parameter("predicate", "condition", version="0.18.9")
    def when(self, condition: IntoExpr) -> ChainedWhen:
        """
        Add a condition to the `when-then-otherwise` expression.

        Parameters
        ----------
        condition
            The condition for applying the subsequent statement.
            Accepts a boolean expression. String input is parsed as a column name.

        """
        condition_pyexpr = parse_as_expression(condition)
        return ChainedWhen(self._then.when(condition_pyexpr))
