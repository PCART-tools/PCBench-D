    @classmethod
    def _from_pyexpr(cls, pyexpr: PyExpr) -> Self:
        expr = cls.__new__(cls)
        expr._pyexpr = pyexpr
        return expr
