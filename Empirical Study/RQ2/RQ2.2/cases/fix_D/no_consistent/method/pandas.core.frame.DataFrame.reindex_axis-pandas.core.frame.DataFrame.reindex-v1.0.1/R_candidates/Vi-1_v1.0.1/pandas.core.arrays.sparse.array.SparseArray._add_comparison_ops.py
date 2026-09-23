    @classmethod
    def _add_comparison_ops(cls):
        cls.__and__ = cls._create_comparison_method(operator.and_)
        cls.__or__ = cls._create_comparison_method(operator.or_)
        cls.__xor__ = cls._create_arithmetic_method(operator.xor)
        super()._add_comparison_ops()
