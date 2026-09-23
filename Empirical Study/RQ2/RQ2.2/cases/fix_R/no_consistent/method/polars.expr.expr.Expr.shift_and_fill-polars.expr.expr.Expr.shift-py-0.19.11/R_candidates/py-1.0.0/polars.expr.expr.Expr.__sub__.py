    def __sub__(self, other: IntoExpr) -> Expr:
        other = parse_into_expression(other)
        return self._from_pyexpr(self._pyexpr - other)
