    @classmethod
    def _add_logical_ops(cls):
        cls.__and__ = cls._create_logical_method(operator.and_)
        cls.__rand__ = cls._create_logical_method(ops.rand_)
        cls.__or__ = cls._create_logical_method(operator.or_)
        cls.__ror__ = cls._create_logical_method(ops.ror_)
        cls.__xor__ = cls._create_logical_method(operator.xor)
        cls.__rxor__ = cls._create_logical_method(ops.rxor)
