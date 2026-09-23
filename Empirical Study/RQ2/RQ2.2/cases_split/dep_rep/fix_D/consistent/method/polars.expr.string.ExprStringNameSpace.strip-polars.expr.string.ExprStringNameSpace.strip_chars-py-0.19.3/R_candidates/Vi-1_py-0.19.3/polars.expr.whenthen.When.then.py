    @deprecate_renamed_parameter("expr", "statement", version="0.18.9")
    def then(self, statement: IntoExpr) -> Then:
        """
        Attach a statement to the corresponding condition.

        Parameters
        ----------
        statement
            The statement to apply if the corresponding condition is true.
            Accepts expression input. Non-expression inputs are parsed as literals.

        """
        if isinstance(statement, str):
            _warn_for_deprecated_string_input_behavior(statement)
        statement_pyexpr = parse_as_expression(statement, str_as_lit=True)
        return Then(self._when.then(statement_pyexpr))
