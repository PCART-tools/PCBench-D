    @unpack_zerodim_and_defer("__divmod__")
    def __divmod__(self, other):
        return self._arith_method(other, divmod)
