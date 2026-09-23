def wrap_expr(pyexpr: PyExpr) -> Expr:
    return pl.Expr._from_pyexpr(pyexpr)
