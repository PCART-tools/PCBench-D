    @unpack_zerodim_and_defer("__truediv__")
    def __truediv__(self, other):
        return self._arith_method(other, operator.truediv)
