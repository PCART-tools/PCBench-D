    @classmethod
    def _from_pyexpr(cls, pyexpr: PyExpr) -> Expr:
        expr = cls.__new__(cls)
        expr._pyexpr = pyexpr
        return expr
