    @classmethod
    def _from_pyexpr(cls, pyexpr: PyExpr) -> Expr:  # type: ignore[override]
        return wrap_expr(pyexpr)
