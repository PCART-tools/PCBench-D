    def _to_expr(self, other: Any) -> Expr:
        if isinstance(other, Expr):
            return other
        return F.lit(other)
