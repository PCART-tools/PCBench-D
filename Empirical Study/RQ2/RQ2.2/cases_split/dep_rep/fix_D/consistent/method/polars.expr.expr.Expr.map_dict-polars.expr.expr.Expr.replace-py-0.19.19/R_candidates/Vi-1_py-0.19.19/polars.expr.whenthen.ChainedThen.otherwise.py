    @deprecate_renamed_parameter("expr", "statement", version="0.18.9")
    def otherwise(self, statement: IntoExpr) -> Expr:
        """
        Define a default for the `when-then-otherwise` expression.

        Parameters
        ----------
        statement
            The statement to apply if all conditions are false.
            Accepts expression input. Non-expression inputs are parsed as literals.

        """
        if isinstance(statement, str):
            _warn_for_deprecated_string_input_behavior(statement)
        statement_pyexpr = parse_as_expression(statement, str_as_lit=True)
        return wrap_expr(self._chained_then.otherwise(statement_pyexpr))
