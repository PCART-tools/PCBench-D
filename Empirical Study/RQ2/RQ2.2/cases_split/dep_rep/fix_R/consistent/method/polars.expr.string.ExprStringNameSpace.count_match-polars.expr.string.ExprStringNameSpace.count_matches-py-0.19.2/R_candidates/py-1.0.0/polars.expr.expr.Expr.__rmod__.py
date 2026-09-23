    def __rmod__(self, other: IntoExpr) -> Expr:
        other = parse_into_expression(other)
        return self._from_pyexpr(other % self._pyexpr)
