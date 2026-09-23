    @unpack_zerodim_and_defer("__rmod__")
    def __rmod__(self, other):
        return self._arith_method(other, roperator.rmod)
