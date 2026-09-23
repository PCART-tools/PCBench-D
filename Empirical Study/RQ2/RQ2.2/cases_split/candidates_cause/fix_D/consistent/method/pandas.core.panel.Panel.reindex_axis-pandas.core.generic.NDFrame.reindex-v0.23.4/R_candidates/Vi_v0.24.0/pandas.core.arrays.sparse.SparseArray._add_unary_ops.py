    @classmethod
    def _add_unary_ops(cls):
        cls.__pos__ = cls._create_unary_method(operator.pos)
        cls.__neg__ = cls._create_unary_method(operator.neg)
        cls.__invert__ = cls._create_unary_method(operator.invert)
