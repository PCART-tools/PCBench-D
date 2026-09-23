    def __gt__(self, other: IntoExpr) -> Expr:
        warn_null_comparison(other)
        other = parse_into_expression(other, str_as_lit=True)
        return self._from_pyexpr(self._pyexpr.gt(other))
