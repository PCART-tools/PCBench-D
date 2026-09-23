    @unpack_zerodim_and_defer("__rpow__")
    def __rpow__(self, other):
        return self._arith_method(other, roperator.rpow)
