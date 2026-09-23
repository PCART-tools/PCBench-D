    def __add__(self, other: IntoExpr) -> Self:
        other = parse_as_expression(other, str_as_lit=True)
        return self._from_pyexpr(self._pyexpr + other)
