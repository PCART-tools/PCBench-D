    @unpack_zerodim_and_defer("__xor__")
    def __xor__(self, other):
        return self._logical_method(other, operator.xor)
