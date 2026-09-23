    def __ror__(self, other: IntoExprColumn | int | bool) -> Expr:
        other_expr = parse_into_expression(other)
        return self._from_pyexpr(other_expr.or_(self._pyexpr))
