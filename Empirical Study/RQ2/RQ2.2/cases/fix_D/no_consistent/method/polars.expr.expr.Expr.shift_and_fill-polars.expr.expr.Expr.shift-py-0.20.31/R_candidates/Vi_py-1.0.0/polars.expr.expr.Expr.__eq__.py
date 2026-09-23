    def __eq__(self, other: IntoExpr) -> Expr:  # type: ignore[override]
        warn_null_comparison(other)
        other = parse_into_expression(other, str_as_lit=True)
        return self._from_pyexpr(self._pyexpr.eq(other))
