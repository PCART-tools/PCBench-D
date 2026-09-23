    def __new__(cls, arg1, arg2, condition=None, **kwargs):
        arg1 = _sympify(arg1)
        arg2 = _sympify(arg2)

        if kwargs.pop('evaluate', global_evaluate[0]):
            arg1, arg2 = sorted([arg1, arg2], key=default_sort_key)

        if condition is None:
            obj = Expr.__new__(cls, arg1, arg2)
        else:
            condition = _sympify(condition)
            obj = Expr.__new__(cls, arg1, arg2, condition)
        obj._condition = condition
        return obj
