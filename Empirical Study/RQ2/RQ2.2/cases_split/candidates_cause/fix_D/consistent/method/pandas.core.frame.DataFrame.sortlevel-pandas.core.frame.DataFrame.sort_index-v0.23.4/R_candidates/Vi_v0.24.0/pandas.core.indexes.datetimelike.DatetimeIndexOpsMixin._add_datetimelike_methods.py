    @classmethod
    def _add_datetimelike_methods(cls):
        """
        Add in the datetimelike methods (as we may have to override the
        superclass).
        """

        def __add__(self, other):
            # dispatch to ExtensionArray implementation
            result = self._data.__add__(maybe_unwrap_index(other))
            return wrap_arithmetic_op(self, other, result)

        cls.__add__ = __add__

        def __radd__(self, other):
            # alias for __add__
            return self.__add__(other)
        cls.__radd__ = __radd__

        def __sub__(self, other):
            # dispatch to ExtensionArray implementation
            result = self._data.__sub__(maybe_unwrap_index(other))
            return wrap_arithmetic_op(self, other, result)

        cls.__sub__ = __sub__

        def __rsub__(self, other):
            result = self._data.__rsub__(maybe_unwrap_index(other))
            return wrap_arithmetic_op(self, other, result)

        cls.__rsub__ = __rsub__
