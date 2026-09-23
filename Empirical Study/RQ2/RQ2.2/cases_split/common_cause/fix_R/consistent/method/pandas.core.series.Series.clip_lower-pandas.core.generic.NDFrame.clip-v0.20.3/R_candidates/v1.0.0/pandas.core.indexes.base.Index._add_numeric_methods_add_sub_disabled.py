    @classmethod
    def _add_numeric_methods_add_sub_disabled(cls):
        """
        Add in the numeric add/sub methods to disable.
        """
        cls.__add__ = make_invalid_op("__add__")
        cls.__radd__ = make_invalid_op("__radd__")
        cls.__iadd__ = make_invalid_op("__iadd__")
        cls.__sub__ = make_invalid_op("__sub__")
        cls.__rsub__ = make_invalid_op("__rsub__")
        cls.__isub__ = make_invalid_op("__isub__")
