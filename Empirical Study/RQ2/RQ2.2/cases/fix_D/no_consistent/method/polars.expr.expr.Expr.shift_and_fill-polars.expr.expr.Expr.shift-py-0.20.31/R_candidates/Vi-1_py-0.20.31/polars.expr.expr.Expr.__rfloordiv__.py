    def __rfloordiv__(self, other: IntoExpr) -> Self:
        other = parse_as_expression(other)
        return self._from_pyexpr(other // self._pyexpr)
