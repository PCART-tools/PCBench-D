    @classmethod
    def _add_arithmetic_ops(cls):
        cls.__add__ = cls._create_arithmetic_method(operator.add)
        cls.__radd__ = cls._create_arithmetic_method(ops.radd)
        cls.__sub__ = cls._create_arithmetic_method(operator.sub)
        cls.__rsub__ = cls._create_arithmetic_method(ops.rsub)
        cls.__mul__ = cls._create_arithmetic_method(operator.mul)
        cls.__rmul__ = cls._create_arithmetic_method(ops.rmul)
        cls.__pow__ = cls._create_arithmetic_method(operator.pow)
        cls.__rpow__ = cls._create_arithmetic_method(ops.rpow)
        cls.__mod__ = cls._create_arithmetic_method(operator.mod)
        cls.__rmod__ = cls._create_arithmetic_method(ops.rmod)
        cls.__floordiv__ = cls._create_arithmetic_method(operator.floordiv)
        cls.__rfloordiv__ = cls._create_arithmetic_method(ops.rfloordiv)
        cls.__truediv__ = cls._create_arithmetic_method(operator.truediv)
        cls.__rtruediv__ = cls._create_arithmetic_method(ops.rtruediv)
        if not PY3:
            cls.__div__ = cls._create_arithmetic_method(operator.div)
            cls.__rdiv__ = cls._create_arithmetic_method(ops.rdiv)

        cls.__divmod__ = cls._create_arithmetic_method(divmod)
        cls.__rdivmod__ = cls._create_arithmetic_method(ops.rdivmod)
