    def __xor__(self, other: IntoExprColumn | int | bool) -> Self:
        other = parse_as_expression(other)
        return self._from_pyexpr(self._pyexpr.xor_(other))
