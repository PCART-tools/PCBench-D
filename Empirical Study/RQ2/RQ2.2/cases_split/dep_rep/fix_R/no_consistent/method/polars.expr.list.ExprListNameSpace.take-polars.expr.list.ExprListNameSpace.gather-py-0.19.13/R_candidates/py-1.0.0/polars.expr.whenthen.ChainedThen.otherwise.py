    def otherwise(self, statement: IntoExpr) -> Expr:
        """
        Define a default for the `when-then-otherwise` expression.

        Parameters
        ----------
        statement
            The statement to apply if all conditions are false.
            Accepts expression input. Strings are parsed as column names, other
            non-expression inputs are parsed as literals.
        """
        statement_pyexpr = parse_into_expression(statement)
        return wrap_expr(self._chained_then.otherwise(statement_pyexpr))
