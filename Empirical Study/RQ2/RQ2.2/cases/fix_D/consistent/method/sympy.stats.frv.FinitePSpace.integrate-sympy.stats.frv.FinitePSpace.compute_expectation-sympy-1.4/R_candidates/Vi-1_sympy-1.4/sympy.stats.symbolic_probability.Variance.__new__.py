    def __new__(cls, arg, condition=None, **kwargs):
        arg = _sympify(arg)
        if condition is None:
            obj = Expr.__new__(cls, arg)
        else:
            condition = _sympify(condition)
            obj = Expr.__new__(cls, arg, condition)
        obj._condition = condition
        return obj
