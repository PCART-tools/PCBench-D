    @unpack_zerodim_and_defer("__mod__")
    def __mod__(self, other):
        return self._arith_method(other, operator.mod)
