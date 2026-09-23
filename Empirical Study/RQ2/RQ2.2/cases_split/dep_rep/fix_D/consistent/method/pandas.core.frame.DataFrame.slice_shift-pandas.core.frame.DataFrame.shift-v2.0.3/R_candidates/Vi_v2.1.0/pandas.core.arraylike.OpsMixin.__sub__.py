    @unpack_zerodim_and_defer("__sub__")
    def __sub__(self, other):
        return self._arith_method(other, operator.sub)
