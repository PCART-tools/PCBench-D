    def __rpow__(self, base: IntoExprColumn | int | float) -> Expr:
        base = parse_into_expression(base)
        return self._from_pyexpr(base) ** self
