    def __truediv__(self, other: IntoExpr) -> Self:
        other = parse_as_expression(other)
        return self._from_pyexpr(self._pyexpr / other)
