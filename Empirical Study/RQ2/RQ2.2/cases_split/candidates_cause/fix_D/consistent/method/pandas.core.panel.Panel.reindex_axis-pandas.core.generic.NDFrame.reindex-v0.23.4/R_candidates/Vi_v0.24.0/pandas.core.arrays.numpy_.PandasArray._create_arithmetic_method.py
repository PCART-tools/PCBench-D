    @classmethod
    def _create_arithmetic_method(cls, op):
        def arithmetic_method(self, other):
            if isinstance(other, (ABCIndexClass, ABCSeries)):
                return NotImplemented

            elif isinstance(other, cls):
                other = other._ndarray

            with np.errstate(all="ignore"):
                result = op(self._ndarray, other)

            if op is divmod:
                a, b = result
                return cls(a), cls(b)

            return cls(result)

        return compat.set_function_name(arithmetic_method,
                                        "__{}__".format(op.__name__),
                                        cls)
