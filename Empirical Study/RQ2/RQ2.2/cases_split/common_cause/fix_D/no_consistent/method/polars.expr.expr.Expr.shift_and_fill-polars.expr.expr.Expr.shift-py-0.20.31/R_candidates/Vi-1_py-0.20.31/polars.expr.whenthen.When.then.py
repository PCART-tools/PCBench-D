    def then(self, statement: IntoExpr) -> Then:
        """
        Attach a statement to the corresponding condition.

        Parameters
        ----------
        statement
            The statement to apply if the corresponding condition is true.
            Accepts expression input. Strings are parsed as column names, other
            non-expression inputs are parsed as literals.
        """
        statement_pyexpr = parse_as_expression(statement)
        return Then(self._when.then(statement_pyexpr))
