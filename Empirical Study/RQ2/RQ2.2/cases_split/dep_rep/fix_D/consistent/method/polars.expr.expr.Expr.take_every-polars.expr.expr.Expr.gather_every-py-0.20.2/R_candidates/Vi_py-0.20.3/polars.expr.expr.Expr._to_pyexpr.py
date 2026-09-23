    def _to_pyexpr(self, other: Any) -> PyExpr:
        if isinstance(other, Expr):
            return other._pyexpr
        else:
            return F.lit(other)._pyexpr
