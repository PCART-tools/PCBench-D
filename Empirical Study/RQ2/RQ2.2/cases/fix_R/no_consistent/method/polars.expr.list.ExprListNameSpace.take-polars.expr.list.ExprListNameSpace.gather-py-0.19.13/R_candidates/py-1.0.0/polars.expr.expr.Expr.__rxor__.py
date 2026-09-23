    def __rxor__(self, other: IntoExprColumn | int | bool) -> Expr:
        other_expr = parse_into_expression(other)
        return self._from_pyexpr(other_expr.xor_(self._pyexpr))
