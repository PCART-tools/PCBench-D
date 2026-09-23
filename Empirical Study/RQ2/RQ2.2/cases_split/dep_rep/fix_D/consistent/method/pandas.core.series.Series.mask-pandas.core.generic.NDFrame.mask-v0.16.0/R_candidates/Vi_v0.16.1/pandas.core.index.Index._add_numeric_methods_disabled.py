    @classmethod
    def _add_numeric_methods_disabled(cls):
        """ add in numeric methods to disable """

        def _make_invalid_op(name):

            def invalid_op(self, other=None):
                raise TypeError("cannot perform {name} with this index type: {typ}".format(name=name,
                                                                                           typ=type(self)))
            invalid_op.__name__ = name
            return invalid_op

        cls.__mul__ = cls.__rmul__ = _make_invalid_op('__mul__')
        cls.__floordiv__ = cls.__rfloordiv__ = _make_invalid_op('__floordiv__')
        cls.__truediv__ = cls.__rtruediv__ = _make_invalid_op('__truediv__')
        if not compat.PY3:
            cls.__div__ = cls.__rdiv__ = _make_invalid_op('__div__')
        cls.__neg__ = _make_invalid_op('__neg__')
        cls.__pos__ = _make_invalid_op('__pos__')
        cls.__abs__ = _make_invalid_op('__abs__')
        cls.__inv__ = _make_invalid_op('__inv__')
