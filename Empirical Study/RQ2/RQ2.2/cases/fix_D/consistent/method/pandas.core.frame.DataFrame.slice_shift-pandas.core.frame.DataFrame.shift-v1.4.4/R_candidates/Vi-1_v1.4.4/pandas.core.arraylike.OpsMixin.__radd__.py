    @unpack_zerodim_and_defer("__radd__")
    def __radd__(self, other):
        return self._arith_method(other, roperator.radd)
