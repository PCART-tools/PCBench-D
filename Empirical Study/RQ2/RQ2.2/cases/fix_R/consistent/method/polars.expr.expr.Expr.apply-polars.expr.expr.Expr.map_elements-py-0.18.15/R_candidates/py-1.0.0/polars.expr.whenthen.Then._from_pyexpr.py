    @classmethod
    def _from_pyexpr(cls, pyexpr: PyExpr) -> Expr:
        return wrap_expr(pyexpr)
