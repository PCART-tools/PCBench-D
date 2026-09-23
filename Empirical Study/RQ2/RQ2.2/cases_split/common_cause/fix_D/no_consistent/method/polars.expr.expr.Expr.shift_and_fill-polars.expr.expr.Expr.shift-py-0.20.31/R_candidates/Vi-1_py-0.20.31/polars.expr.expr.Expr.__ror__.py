    def __ror__(self, other: IntoExprColumn | int | bool) -> Self:
        other_expr = parse_as_expression(other)
        return self._from_pyexpr(other_expr.or_(self._pyexpr))
