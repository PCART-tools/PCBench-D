    def __pow__(self, exponent: IntoExprColumn | int | float) -> Self:
        exponent = parse_as_expression(exponent)
        return self._from_pyexpr(self._pyexpr.pow(exponent))
