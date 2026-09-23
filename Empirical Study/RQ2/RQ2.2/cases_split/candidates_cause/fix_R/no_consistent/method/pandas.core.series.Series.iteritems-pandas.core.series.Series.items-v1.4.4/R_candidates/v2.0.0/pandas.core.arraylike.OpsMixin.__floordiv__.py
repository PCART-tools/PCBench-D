    @unpack_zerodim_and_defer("__floordiv__")
    def __floordiv__(self, other):
        return self._arith_method(other, operator.floordiv)
