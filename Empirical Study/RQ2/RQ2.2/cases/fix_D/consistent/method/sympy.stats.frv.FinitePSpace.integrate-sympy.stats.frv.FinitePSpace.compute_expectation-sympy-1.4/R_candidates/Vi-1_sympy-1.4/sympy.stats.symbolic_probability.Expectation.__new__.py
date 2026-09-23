    def __new__(cls, expr, condition=None, **kwargs):
        expr = _sympify(expr)
        if condition is None:
            if not expr.has(RandomSymbol):
                return expr
            obj = Expr.__new__(cls, expr)
        else:
            condition = _sympify(condition)
            obj = Expr.__new__(cls, expr, condition)
        obj._condition = condition
        return obj
