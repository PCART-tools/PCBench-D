    def __add__(self, other: IntoExpr) -> Expr:
        other = parse_into_expression(other, str_as_lit=True)
        return self._from_pyexpr(self._pyexpr + other)
