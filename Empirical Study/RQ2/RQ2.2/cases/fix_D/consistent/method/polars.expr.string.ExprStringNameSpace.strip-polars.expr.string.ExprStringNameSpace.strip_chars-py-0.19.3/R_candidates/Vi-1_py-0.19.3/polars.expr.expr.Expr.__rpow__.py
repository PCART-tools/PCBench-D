    def __rpow__(self, base: int | float | Expr) -> Expr:
        return self._from_pyexpr(parse_as_expression(base)) ** self
