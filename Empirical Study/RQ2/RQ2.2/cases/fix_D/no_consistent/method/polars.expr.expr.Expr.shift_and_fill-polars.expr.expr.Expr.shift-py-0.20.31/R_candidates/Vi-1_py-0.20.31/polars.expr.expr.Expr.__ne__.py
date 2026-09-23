    def __ne__(self, other: IntoExpr) -> Self:  # type: ignore[override]
        warn_null_comparison(other)
        other = parse_as_expression(other, str_as_lit=True)
        return self._from_pyexpr(self._pyexpr.neq(other))
