    @classmethod
    def _add_comparison_ops(cls):
        cls.__eq__ = cls._create_comparison_method(operator.eq)
        cls.__ne__ = cls._create_comparison_method(operator.ne)
        cls.__lt__ = cls._create_comparison_method(operator.lt)
        cls.__gt__ = cls._create_comparison_method(operator.gt)
        cls.__le__ = cls._create_comparison_method(operator.le)
        cls.__ge__ = cls._create_comparison_method(operator.ge)
