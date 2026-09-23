    def __pow__(self, exponent: IntoExprColumn | int | float) -> Expr:
        exponent = parse_into_expression(exponent)
        return self._from_pyexpr(self._pyexpr.pow(exponent))
