    @classmethod
    def _add_numeric_methods_disabled(cls):
        """
        Add in numeric methods to disable other than add/sub.
        """
        cls.__pow__ = make_invalid_op('__pow__')
        cls.__rpow__ = make_invalid_op('__rpow__')
        cls.__mul__ = make_invalid_op('__mul__')
        cls.__rmul__ = make_invalid_op('__rmul__')
        cls.__floordiv__ = make_invalid_op('__floordiv__')
        cls.__rfloordiv__ = make_invalid_op('__rfloordiv__')
        cls.__truediv__ = make_invalid_op('__truediv__')
        cls.__rtruediv__ = make_invalid_op('__rtruediv__')
        if not compat.PY3:
            cls.__div__ = make_invalid_op('__div__')
            cls.__rdiv__ = make_invalid_op('__rdiv__')
        cls.__mod__ = make_invalid_op('__mod__')
        cls.__divmod__ = make_invalid_op('__divmod__')
        cls.__neg__ = make_invalid_op('__neg__')
        cls.__pos__ = make_invalid_op('__pos__')
        cls.__abs__ = make_invalid_op('__abs__')
        cls.__inv__ = make_invalid_op('__inv__')
