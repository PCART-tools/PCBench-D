    def __radd__(self, other: IntoExpr) -> Expr:
        other = parse_into_expression(other, str_as_lit=True)
        return self._from_pyexpr(other + self._pyexpr)
