    @unpack_zerodim_and_defer("__rsub__")
    def __rsub__(self, other):
        return self._arith_method(other, roperator.rsub)
