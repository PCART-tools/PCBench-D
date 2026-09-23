    @unpack_zerodim_and_defer("__rfloordiv")
    def __rfloordiv__(self, other):
        return self._arith_method(other, roperator.rfloordiv)
