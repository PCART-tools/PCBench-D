    @unpack_zerodim_and_defer("__mul__")
    def __mul__(self, other):
        return self._arith_method(other, operator.mul)
