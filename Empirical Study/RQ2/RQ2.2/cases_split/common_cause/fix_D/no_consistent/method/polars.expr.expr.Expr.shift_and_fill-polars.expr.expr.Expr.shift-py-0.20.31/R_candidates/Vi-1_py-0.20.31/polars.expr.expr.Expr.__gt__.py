    def __gt__(self, other: IntoExpr) -> Self:
        warn_null_comparison(other)
        other = parse_as_expression(other, str_as_lit=True)
        return self._from_pyexpr(self._pyexpr.gt(other))
