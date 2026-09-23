    @classmethod
    def _add_numeric_methods_binary(cls):
        """ add in numeric methods """
        cls.__add__ = _make_arithmetic_op(operator.add, cls)
        cls.__radd__ = _make_arithmetic_op(ops.radd, cls)
        cls.__sub__ = _make_arithmetic_op(operator.sub, cls)
        cls.__rsub__ = _make_arithmetic_op(ops.rsub, cls)
        cls.__mul__ = _make_arithmetic_op(operator.mul, cls)
        cls.__rmul__ = _make_arithmetic_op(ops.rmul, cls)
        cls.__rpow__ = _make_arithmetic_op(ops.rpow, cls)
        cls.__pow__ = _make_arithmetic_op(operator.pow, cls)
        cls.__mod__ = _make_arithmetic_op(operator.mod, cls)
        cls.__floordiv__ = _make_arithmetic_op(operator.floordiv, cls)
        cls.__rfloordiv__ = _make_arithmetic_op(ops.rfloordiv, cls)
        cls.__truediv__ = _make_arithmetic_op(operator.truediv, cls)
        cls.__rtruediv__ = _make_arithmetic_op(ops.rtruediv, cls)
        if not compat.PY3:
            cls.__div__ = _make_arithmetic_op(operator.div, cls)
            cls.__rdiv__ = _make_arithmetic_op(ops.rdiv, cls)

        cls.__divmod__ = _make_arithmetic_op(divmod, cls)
