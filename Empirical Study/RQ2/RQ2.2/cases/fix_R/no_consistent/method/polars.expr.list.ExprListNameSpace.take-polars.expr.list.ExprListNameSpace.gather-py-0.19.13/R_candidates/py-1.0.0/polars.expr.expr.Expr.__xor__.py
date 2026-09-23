    def __xor__(self, other: IntoExprColumn | int | bool) -> Expr:
        other = parse_into_expression(other)
        return self._from_pyexpr(self._pyexpr.xor_(other))
