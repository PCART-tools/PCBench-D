    def __rxor__(self, other: IntoExprColumn | int | bool) -> Self:
        other_expr = parse_as_expression(other)
        return self._from_pyexpr(other_expr.xor_(self._pyexpr))
