    @unpack_zerodim_and_defer("__pow__")
    def __pow__(self, other):
        return self._arith_method(other, operator.pow)
