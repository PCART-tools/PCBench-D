    def __rpow__(self, base: IntoExprColumn | int | float) -> Expr:
        base = parse_as_expression(base)
        return self._from_pyexpr(base) ** self
